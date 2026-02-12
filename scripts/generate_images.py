"""
Daily AI Image Generator for sB Countdown
Uses Google Gemini (Imagen) to generate fresh countdown images.
Runs via GitHub Actions on a daily cron schedule.
"""

import os
import sys
import base64
from datetime import date, datetime
from google import genai
from google.genai import types

# =============================================
# CONFIGURATION
# =============================================
API_KEY = os.environ.get('GEMINI_API_KEY')
if not API_KEY:
    print("ERROR: GEMINI_API_KEY environment variable not set!")
    sys.exit(1)

# Target dates
USA_HONEYMOON_DATE = date(2026, 6, 7)
DOLOMITES_DATE = date(2026, 5, 4)

# Output paths
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')

# =============================================
# PROMPTS
# =============================================
def get_usa_prompt(days_remaining):
    return (
        f'A cinematic, high-resolution 16:9 landscape photograph of a famous California location '
        f'during golden hour. The landscape should fill the entire frame with NO heart shapes, '
        f'NO frames, NO borders overlaid on the scenery. Show a different iconic spot each time: '
        f'Hollywood sign from behind, Golden Gate Bridge at sunset, Big Sur cliffs, Yosemite valley, '
        f'Pacific Coast Highway, or Napa Valley vineyards. '
        f'In the upper portion of the image, overlay clean elegant white cursive script text that reads: '
        f'"there are only {days_remaining} days to our US Honeymoon". '
        f'In the bottom right corner only, place a very small minimalist white heart outline with '
        f'the letters "sB" inside it, and directly below it in small clean sans-serif font, '
        f'the name of the location shown (e.g. "Hollywood, Los Angeles, California"). '
        f'The overall look should be like a premium travel postcard — romantic, airy, and elegant. '
        f'Do NOT add any heart shapes or decorative frames over the landscape itself.'
    )

def get_dolomites_prompt(days_remaining):
    return (
        f'A cinematic, high-resolution 16:9 landscape photograph of the Dolomites, Italy '
        f'during sunrise or sunset. The landscape should fill the entire frame with NO heart shapes, '
        f'NO frames, NO borders overlaid on the scenery. Show iconic Dolomites scenery: '
        f'jagged limestone peaks, alpine meadows with wildflowers, a rustic mountain hut, '
        f'Lago di Braies, Seceda ridgeline, or Tre Cime di Lavaredo. '
        f'In the upper portion of the image, overlay clean elegant white cursive script text that reads: '
        f'"there are only {days_remaining} days to our Dolomites Minimoon". '
        f'In the bottom right corner only, place a very small minimalist white heart outline with '
        f'the letters "sB" inside it, and directly below it in small clean sans-serif font, '
        f'the text "Dolomites, Italy". '
        f'The overall look should be like a premium travel postcard — romantic, airy, and elegant. '
        f'Do NOT add any heart shapes or decorative frames over the landscape itself.'
    )

# =============================================
# IMAGE GENERATION
# =============================================
def generate_image(prompt, output_filename):
    """Generate an image using Gemini and save it."""
    print(f"\n🎨 Generating: {output_filename}")
    print(f"📝 Prompt: {prompt[:100]}...")

    client = genai.Client(api_key=API_KEY)
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    # Try with gemini-2.5-flash (Nano Banana) - image generation via generateContent
    models_to_try = ['gemini-2.0-flash-exp-image-generation', 'gemini-2.0-flash-exp']

    for model_name in models_to_try:
        try:
            print(f"🔄 Trying model: {model_name}")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['IMAGE', 'TEXT']
                )
            )

            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.mime_type.startswith('image/'):
                    with open(output_path, 'wb') as f:
                        f.write(part.inline_data.data)
                    print(f"✅ Saved to: {output_path}")
                    return True

            print(f"⚠️ No image in response from {model_name}")

        except Exception as e:
            print(f"❌ Error with {model_name}: {e}")

    # Fallback: try Imagen 3
    try:
        print("🔄 Trying fallback: imagen-3.0-generate-002")
        response = client.models.generate_images(
            model='imagen-3.0-generate-002',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio='16:9',
            )
        )

        if response.generated_images:
            image = response.generated_images[0]
            image.image.save(output_path)
            print(f"✅ Saved (Imagen) to: {output_path}")
            return True

    except Exception as e:
        print(f"❌ Imagen fallback error: {e}")

    print(f"❌ All models failed for {output_filename}")
    return False

# =============================================
# MAIN
# =============================================
def main():
    today = date.today()
    print(f"📅 Date: {today}")
    print(f"📁 Output: {OUTPUT_DIR}")

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Calculate days remaining
    usa_days = (USA_HONEYMOON_DATE - today).days
    dolomites_days = (DOLOMITES_DATE - today).days

    print(f"\n🇺🇸 USA Honeymoon: {usa_days} days remaining")
    print(f"🇮🇹 Dolomites Minimoon: {dolomites_days} days remaining")

    success_count = 0

    # Generate USA image (only if trip hasn't passed)
    if usa_days > 0:
        usa_prompt = get_usa_prompt(usa_days)
        if generate_image(usa_prompt, 'usa-honeymoon.png'):
            success_count += 1
    else:
        print("🇺🇸 USA Honeymoon date has passed, skipping.")

    # Generate Dolomites image (only if trip hasn't passed)
    if dolomites_days > 0:
        dolomites_prompt = get_dolomites_prompt(dolomites_days)
        if generate_image(dolomites_prompt, 'dolomites-minimoon.png'):
            success_count += 1
    else:
        print("🇮🇹 Dolomites date has passed, skipping.")

    print(f"\n🏁 Done! {success_count} images generated.")

    if success_count == 0:
        print("⚠️ No images were generated!")
        sys.exit(1)

if __name__ == '__main__':
    main()

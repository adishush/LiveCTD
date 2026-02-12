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
        f'A cinematic, high-resolution landscape photograph capturing a random, '
        f'breathtaking scenic view of California during the golden hour (e.g., the rugged '
        f'Big Sur coastline, a misty redwood forest, or the rolling golden hills of Napa Valley). '
        f'Centered on the image is a clear, elegant white script text overlay that reads: '
        f'"there are only {days_remaining} days to our US Honeymoon". '
        f'In the bottom right corner, include a minimalist white heart outline logo with the '
        f'stylized letters "sB" inside; the heart must be transparent so that the landscape '
        f'background "completes" the shape of the heart. Directly below the heart, in an aesthetic '
        f'and clean sans-serif font, add a text label specifying the location pictured '
        f'(e.g., "Big Sur, California"). The overall aesthetic should be romantic, high-end, and airy.'
    )

def get_dolomites_prompt(days_remaining):
    return (
        f'A cinematic, high-resolution landscape photograph capturing a breathtaking, '
        f'diverse scenic view typical of the Dolomites in Italy. The image should feature iconic '
        f'elements of the region, such as jagged limestone peaks, rolling alpine meadows dotted '
        f'with wildflowers, a rustic mountain hut, or a winding trail, all bathed in the warm '
        f'light of sunrise or sunset. Centered on the image is a clear, elegant white script '
        f'text overlay that reads: "there are only {days_remaining} days to our Dolomites Minimoon". '
        f'In the bottom right corner, include a minimalist white heart logo with the stylized '
        f'letters "sB" inside. Directly below the heart, in a small, clean sans-serif font, '
        f'add the text label: "Dolomites, Italy". The overall aesthetic should be romantic, '
        f'airy, and high-end.'
    )

# =============================================
# IMAGE GENERATION
# =============================================
def generate_image(prompt, output_filename):
    """Generate an image using Gemini Imagen and save it."""
    print(f"\n🎨 Generating: {output_filename}")
    print(f"📝 Prompt: {prompt[:100]}...")

    client = genai.Client(api_key=API_KEY)

    try:
        # Use Imagen 3 for high-quality image generation
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
            output_path = os.path.join(OUTPUT_DIR, output_filename)

            # Save image
            image.image.save(output_path)
            print(f"✅ Saved to: {output_path}")
            return True
        else:
            print(f"❌ No images generated")
            return False

    except Exception as e:
        print(f"❌ Error generating image: {e}")

        # Fallback: try with gemini-2.0-flash-exp
        try:
            print("🔄 Trying fallback with gemini-2.0-flash-exp...")
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=f"Generate this image: {prompt}",
                config=types.GenerateContentConfig(
                    response_modalities=['IMAGE', 'TEXT']
                )
            )

            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.mime_type.startswith('image/'):
                    output_path = os.path.join(OUTPUT_DIR, output_filename)
                    with open(output_path, 'wb') as f:
                        f.write(part.inline_data.data)
                    print(f"✅ Saved (fallback) to: {output_path}")
                    return True

            print("❌ Fallback also failed - no image in response")
            return False

        except Exception as e2:
            print(f"❌ Fallback error: {e2}")
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

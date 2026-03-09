#!/usr/bin/env python3
"""
Creative Pitch Generator
========================
Takes brand insights and produces a full creative pitch:
  1. Brand Analysis & Brief
  2. Creative POV (Point of View)
  3. Ad Concepts with Media Strategy
  4. HTML Mock-up of the hero ad

Usage:
  python3 pitch_generator.py --brand "Brand Name" --insights "Brand insights..."
  python3 pitch_generator.py --config brand_config.json
  python3 pitch_generator.py  (interactive mode)
"""

import anthropic
import argparse
import json
import os
import sys
from datetime import datetime


client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"


def call_claude(system_prompt: str, user_prompt: str) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return response.content[0].text


def generate_brief(brand: str, insights: str) -> str:
    system = (
        "You are a world-class creative strategist at a top advertising agency. "
        "You write sharp, insight-driven creative briefs that inspire breakthrough work. "
        "Return your response as structured JSON with these keys: "
        "brand_essence, target_audience, key_insight, brand_tension, "
        "single_minded_proposition, reasons_to_believe (list), tone_and_manner, mandatories (list)"
    )
    prompt = f"""Create a creative brief for {brand}.

Brand insights and context:
{insights}

Return valid JSON only, no markdown fences."""

    raw = call_claude(system, prompt)
    return raw


def generate_pov(brand: str, brief_json: str) -> str:
    system = (
        "You are a creative director known for bold, culture-forward thinking. "
        "You write compelling creative POVs that frame the strategic opportunity "
        "in a way that excites clients and creative teams alike. "
        "Return JSON with keys: pov_title, cultural_context, strategic_opportunity, "
        "creative_territory, brand_role_in_culture, manifesto (a short 4-6 sentence paragraph)"
    )
    prompt = f"""Based on this creative brief for {brand}, develop a creative POV
that captures the strategic and cultural opportunity.

Brief:
{brief_json}

Return valid JSON only, no markdown fences."""

    return call_claude(system, prompt)


def generate_ad_concepts(brand: str, brief_json: str, pov_json: str) -> str:
    system = (
        "You are an award-winning creative team (art director + copywriter) "
        "known for work that wins at Cannes and drives business results. "
        "Return JSON with key 'concepts' containing a list of 3 ad concepts. "
        "Each concept has: concept_name, format (e.g. 'Print/OOH', 'Digital Video', 'Social-First'), "
        "headline, subhead, body_copy (2-3 sentences), visual_description (detailed description "
        "of the visual for the ad), call_to_action, why_it_works (1 sentence)"
    )
    prompt = f"""Create 3 distinct ad concepts for {brand} that bring this POV to life across different media.

Brief:
{brief_json}

Creative POV:
{pov_json}

Make concepts bold, unexpected, and ownable. Each should work in a different format.
Return valid JSON only, no markdown fences."""

    return call_claude(system, prompt)


def generate_media_strategy(brand: str, brief_json: str, concepts_json: str) -> str:
    system = (
        "You are a media strategist who thinks about media as a creative canvas. "
        "Return JSON with keys: media_idea (the overarching media insight), "
        "channels (list of objects with: channel, role, format, timing, rationale), "
        "phasing (list of objects with: phase_name, duration, objective, key_actions), "
        "budget_split (list of objects with: channel, percentage, rationale)"
    )
    prompt = f"""Develop a media strategy for {brand} that amplifies these creative concepts.

Brief:
{brief_json}

Concepts:
{concepts_json}

Think about how media placement itself can be part of the creative idea.
Return valid JSON only, no markdown fences."""

    return call_claude(system, prompt)


def generate_html_mockup(brand: str, brief_json: str, pov_json: str,
                          concepts_json: str, media_json: str) -> str:
    system = (
        "You are a senior designer and front-end developer who creates stunning "
        "pitch deck presentations and ad mock-ups in HTML/CSS. You produce complete, "
        "self-contained HTML files with inline CSS. Use modern design with bold typography, "
        "strong color palettes, and clean layouts. For ad mock-ups, create realistic-looking "
        "ad layouts using CSS shapes, gradients, and typography (no external images needed). "
        "The output should look like a professional agency pitch deck."
    )
    prompt = f"""Create a complete, self-contained HTML pitch deck for {brand}.

The HTML should include ALL of the following sections, beautifully designed:

1. COVER PAGE - Brand name, pitch title, date, agency branding
2. BRAND BRIEF - Display the brief in a clean, scannable layout
3. CREATIVE POV - The strategic point of view with the manifesto as a hero moment
4. AD CONCEPTS - Show all 3 concepts as cards with visual descriptions
5. HERO AD MOCK-UP - Create a FULL visual mock-up of Concept 1 as if it were a real ad.
   Use CSS to create the visual layout: background gradients/colors, bold typography for
   headline and subhead, body copy placement, CTA button, and visual elements described
   in the concept. Make this look like a real print/digital ad, not just text on a page.
6. MEDIA STRATEGY - Channel mix, phasing timeline, budget allocation (use a simple CSS bar chart)
7. SUMMARY PAGE - Key takeaways

Design requirements:
- Use a cohesive color palette appropriate for the brand
- Bold, modern typography (use system fonts and Google Fonts via CDN)
- Each section should be a full-viewport "slide"
- Include smooth scroll-snap for a slide-deck feel
- Add subtle CSS animations on scroll
- The hero ad mock-up should be the showpiece - make it look like a real advertisement
- Responsive design that works on desktop

BRAND BRIEF:
{brief_json}

CREATIVE POV:
{pov_json}

AD CONCEPTS:
{concepts_json}

MEDIA STRATEGY:
{media_json}

Return ONLY the complete HTML document, no markdown fences or explanation."""

    return call_claude(system, prompt)


def run_pitch(brand: str, insights: str, output_dir: str = None):
    if not output_dir:
        output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    slug = brand.lower().replace(" ", "-")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    print(f"\n{'='*60}")
    print(f"  CREATIVE PITCH GENERATOR")
    print(f"  Brand: {brand}")
    print(f"{'='*60}\n")

    # Stage 1: Brief
    print("[1/5] Generating creative brief...")
    brief_raw = generate_brief(brand, insights)
    try:
        brief = json.loads(brief_raw)
        brief_json = json.dumps(brief, indent=2)
    except json.JSONDecodeError:
        brief_json = brief_raw
    print("      Done.\n")

    # Stage 2: POV
    print("[2/5] Developing creative POV...")
    pov_raw = generate_pov(brand, brief_json)
    try:
        pov = json.loads(pov_raw)
        pov_json = json.dumps(pov, indent=2)
    except json.JSONDecodeError:
        pov_json = pov_raw
    print("      Done.\n")

    # Stage 3: Ad Concepts
    print("[3/5] Creating ad concepts...")
    concepts_raw = generate_ad_concepts(brand, brief_json, pov_json)
    try:
        concepts = json.loads(concepts_raw)
        concepts_json = json.dumps(concepts, indent=2)
    except json.JSONDecodeError:
        concepts_json = concepts_raw
    print("      Done.\n")

    # Stage 4: Media Strategy
    print("[4/5] Building media strategy...")
    media_raw = generate_media_strategy(brand, brief_json, concepts_json)
    try:
        media = json.loads(media_raw)
        media_json = json.dumps(media, indent=2)
    except json.JSONDecodeError:
        media_json = media_raw
    print("      Done.\n")

    # Stage 5: HTML Mock-up
    print("[5/5] Designing pitch deck & ad mock-up...")
    html = generate_html_mockup(brand, brief_json, pov_json, concepts_json, media_json)
    print("      Done.\n")

    # Save outputs
    data_file = os.path.join(output_dir, f"{slug}-{timestamp}-data.json")
    html_file = os.path.join(output_dir, f"{slug}-{timestamp}-pitch.html")

    pitch_data = {
        "brand": brand,
        "insights": insights,
        "generated_at": timestamp,
        "brief": json.loads(brief_json) if brief_json.startswith("{") else brief_json,
        "pov": json.loads(pov_json) if pov_json.startswith("{") else pov_json,
        "concepts": json.loads(concepts_json) if concepts_json.startswith("{") else concepts_json,
        "media_strategy": json.loads(media_json) if media_json.startswith("{") else media_json,
    }

    with open(data_file, "w") as f:
        json.dump(pitch_data, f, indent=2)

    with open(html_file, "w") as f:
        f.write(html)

    print(f"{'='*60}")
    print(f"  PITCH COMPLETE!")
    print(f"  Data: {data_file}")
    print(f"  Deck: {html_file}")
    print(f"{'='*60}\n")

    return html_file, data_file


def main():
    parser = argparse.ArgumentParser(description="Creative Pitch Generator")
    parser.add_argument("--brand", type=str, help="Brand name")
    parser.add_argument("--insights", type=str, help="Brand insights and context")
    parser.add_argument("--config", type=str, help="Path to JSON config file with brand/insights")
    parser.add_argument("--output", type=str, help="Output directory", default=None)
    args = parser.parse_args()

    if args.config:
        with open(args.config) as f:
            config = json.load(f)
        brand = config["brand"]
        insights = config["insights"]
    elif args.brand and args.insights:
        brand = args.brand
        insights = args.insights
    else:
        print("\nCreative Pitch Generator - Interactive Mode\n")
        brand = input("Brand name: ").strip()
        print("\nEnter brand insights (press Enter twice to finish):")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        insights = "\n".join(lines)

    run_pitch(brand, insights, args.output)


if __name__ == "__main__":
    main()

import streamlit as st

import torch
from transformers import pipeline, set_seed
from transformers import AutoTokenizer

from PIL import (
    ImageFont,
)

import os
import re
import random
import textwrap
from examples import EXAMPLES
import dummy
import meta
from utils import ext
from utils.api import generate_cook_image
from utils.draw import generate_food_with_logo_image, generate_recipe_image
from utils.st import (
    remote_css,
    local_css,

)
from utils.utils import (
    load_image_from_url,
    load_image_from_local,
    image_to_base64,
    pure_comma_separation
)


class TextGeneration:
    def __init__(self):
        self.debug = False
        self.dummy_outputs = dummy.recipes
        self.tokenizer = None
        self.generator = None
        self.api_ids = []
        self.api_keys = []
        self.api_test = 2
        self.task = "text-generation"
        self.model_name_or_path = "flax-community/t5-recipe-generation"
        self.color_frame = "#ffffff"
        self.main_frame = "asset/frame/recipe-bg.png"
        self.no_food = "asset/frame/no_food.png"
        self.logo_frame = "asset/frame/logo.png"
        self.chef_frames = {
            "scheherazade": "asset/frame/food-image-logo-bg-s.png",
            "giovanni": "asset/frame/food-image-logo-bg-g.png",
        }
        self.fonts = {
            "title": ImageFont.truetype("asset/fonts/Poppins-Bold.ttf", 70),
            "sub_title": ImageFont.truetype("asset/fonts/Poppins-Medium.ttf", 30),
            "body_bold": ImageFont.truetype("asset/fonts/Montserrat-Bold.ttf", 22),
            "body": ImageFont.truetype("asset/fonts/Montserrat-Regular.ttf", 18),

        }
        set_seed(42)

    def _skip_special_tokens_and_prettify(self, text):
        recipe_maps = {"<sep>": "--", "<section>": "\n"}
        recipe_map_pattern = "|".join(map(re.escape, recipe_maps.keys()))

        text = re.sub(
            recipe_map_pattern,
            lambda m: recipe_maps[m.group()],
            re.sub("|".join(self.tokenizer.all_special_tokens), "", text)
        )

        data = {"title": "", "ingredients": [], "directions": []}
        for section in text.split("\n"):
            section = section.strip()
            if section.startswith("title:"):
                data["title"] = " ".join(
                    [w.strip().capitalize() for w in section.replace("title:", "").strip().split() if w.strip()]
                )
            elif section.startswith("ingredients:"):
                data["ingredients"] = [s.strip() for s in section.replace("ingredients:", "").split('--')]
            elif section.startswith("directions:"):
                data["directions"] = [s.strip() for s in section.replace("directions:", "").split('--')]
            else:
                pass

        return data

    def load_pipeline(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path)
        self.generator = pipeline(self.task, model=self.model_name_or_path, tokenizer=self.model_name_or_path)

    def load_api(self):
        app_ids = os.getenv("EDAMAM_APP_ID")
        app_ids = app_ids.split(",") if app_ids else []
        app_keys = os.getenv("EDAMAM_APP_KEY")
        app_keys = app_keys.split(",") if app_keys else []

        if len(app_ids) != len(app_keys):
            self.api_ids = []
            self.api_keys = []

        self.api_ids = app_ids
        self.api_keys = app_keys

    def load(self):
        self.load_api()
        if not self.debug:
            self.load_pipeline()

    def prepare_frame(self, recipe, chef_name):
        frame_path = self.chef_frames[chef_name.lower()]
        food_logo = generate_food_with_logo_image(frame_path, self.logo_frame, recipe["image"])
        frame = generate_recipe_image(
            recipe,
            self.main_frame,
            food_logo,
            self.fonts,
            bg_color="#ffffff"
        )
        return frame

    def generate(self, items, generation_kwargs):
        recipe = self.dummy_outputs[0]
        # recipe = self.dummy_outputs[random.randint(0, len(self.dummy_outputs) - 1)]

        if not self.debug:
            generation_kwargs["num_return_sequences"] = 1
            # generation_kwargs["return_full_text"] = False
            generation_kwargs["return_tensors"] = True

            generated_ids = self.generator(
                items,
                **generation_kwargs,
            )[0]["generated_token_ids"]
            recipe = self.tokenizer.decode(generated_ids, skip_special_tokens=False)
            recipe = self._skip_special_tokens_and_prettify(recipe)

        if self.api_ids and self.api_keys and len(self.api_ids) == len(self.api_keys):
            test = 0
            for i in range(len(self.api_keys)):
                if test > self.api_test:
                    recipe["image"] = None
                    break
                image = generate_cook_image(recipe["title"].lower(), self.api_ids[i], self.api_keys[i])
                test += 1
                if image:
                    recipe["image"] = image
                    break
        else:
            recipe["image"] = None

        return recipe

    def generate_frame(self, recipe, chef_name):
        return self.prepare_frame(recipe, chef_name)


@st.cache(allow_output_mutation=True)
def load_text_generator():
    generator = TextGeneration()
    generator.load()
    return generator


chef_top = {
    "max_length": 512,
    "min_length": 64,
    "no_repeat_ngram_size": 3,
    "do_sample": True,
    "top_k": 60,
    "top_p": 0.95,
    "num_return_sequences": 1
}
chef_beam = {
    "max_length": 512,
    "min_length": 64,
    "no_repeat_ngram_size": 3,
    "early_stopping": True,
    "num_beams": 5,
    "length_penalty": 1.5,
    "num_return_sequences": 1
}


def main():
    st.set_page_config(
        page_title="Chef Transformer",
        page_icon="🍲",
        layout="centered"  # changed from wide
    )

    generator = load_text_generator()

    remote_css("https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&family=Poppins:wght@600&display=swap")
    local_css("asset/css/style.css")

    # 🔥 Header (clean + centered)
    st.markdown(meta.HEADER_INFO, unsafe_allow_html=True)

    # Inputs layout inside columns
    col1, col2 = st.columns(2)
    with col1:
        chef = st.selectbox(
            "👨‍🍳 Choose Your Chef",
            index=0,
            options=["Chef Scheherazade", "Chef Giovanni"]
        )

    with col2:
        prompts = list(EXAMPLES.keys()) + ["Custom"]
        prompt = st.selectbox(
            '🍽️ Try an Example',
            prompts,
            index=0
        )

    if prompt == "Custom":
        prompt_box = ""
    else:
        prompt_box = EXAMPLES[prompt]

    # Input
    items = st.text_area(
        '📝 Enter Ingredients (comma separated)',
        pure_comma_separation(prompt_box, return_list=False),
        height=120
    )

    items = pure_comma_separation(items, return_list=False)
    entered_items = st.empty()

    # Button (center focus)
    recipe_button = st.button('🔥 Generate Recipe')

    st.markdown("<hr />", unsafe_allow_html=True)

    # 🔥 OUTPUT SECTION
    if recipe_button:
        entered_items.markdown("**Generating recipe for:** " + items)

        with st.spinner("👨‍🍳 Cooking your recipe..."):
            if not isinstance(items, str) or not len(items) > 1:
                st.warning("Please enter valid ingredients!")
            else:
                gen_kw = chef_top if chef == "Chef Scheherazade" else chef_beam
                generated_recipe = generator.generate(items, gen_kw)

                title = generated_recipe["title"]

                food_image = generated_recipe["image"]
                food_image = load_image_from_url(food_image, rgba_mode=True, default_image=generator.no_food)
                food_image = image_to_base64(food_image)

                ingredients = ext.ingredients(
                    generated_recipe["ingredients"],
                    pure_comma_separation(items, return_list=True)
                )

                directions = ext.directions(generated_recipe["directions"])
                generated_recipe["by"] = chef

                # 🔥 NEW CLEAN LAYOUT (stacked instead of side-by-side)
                recipe_html = f"""<div class="recipe-card">
<h2 class="recipe-title">🍜 {title}</h2>
<div class="recipe-image-wrapper">
<img class="recipe-image" src="{food_image}" width="250" />
</div>
<div class="ingredients-section">
<h3>🧂 Ingredients</h3>
<ul style="list-style-type: none; padding-left: 0; margin-left: 0;">"""
                for item in ingredients:
                    recipe_html += f'<li class="ingredient-item">{item}</li>'
                
                recipe_html += """</ul>
</div>
<div class="directions-section">
<h3>👨‍🍳 Directions</h3>
<ol style="padding-left: 20px; margin-left: 0; color: #cbd5e1;">"""
                for step in directions:
                    recipe_html += f'<li class="direction-item">{step}</li>'
                
                recipe_html += """</ol>
</div>
</div>"""
                st.markdown(recipe_html, unsafe_allow_html=True)

                # Optional image card (kept but cleaner)
                st.markdown("### 📸 Shareable Recipe Card")

                recipe_post = generator.generate_frame(generated_recipe, chef.split()[-1])

                st.image(
                    recipe_post,
                    caption="Save & share your recipe!",
                    use_column_width=True
                )


if __name__ == '__main__':
    main()

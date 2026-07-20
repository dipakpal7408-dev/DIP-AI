"""
DIP AI V-01 — high quality image generation demo
Gradio app for Hugging Face Spaces.

HOW TO WIRE IN YOUR MODEL
-------------------------
This file ships with a working placeholder pipeline (Stable Diffusion via
diffusers) so the Space runs out of the box. Swap the load_model() and
generate() functions below for your own DIP AI V-01 code from your GitHub
repo, then update requirements.txt to match your model's dependencies.

Two common ways to bring in your own repo code:

1) Vendor your repo folder straight into this Space folder (e.g. a `dip_ai/`
   package next to app.py) and import it:
       from dip_ai import load_model, generate_image

2) Pull weights from the Hugging Face Hub at startup:
       from huggingface_hub import hf_hub_download
       ckpt_path = hf_hub_download(repo_id="your-username/dip-ai-v01", filename="model.safetensors")
"""

import gradio as gr
import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32

_pipe = None


def load_model():
    """Load the model once and cache it. Replace this with your DIP AI V-01 loader."""
    global _pipe
    if _pipe is not None:
        return _pipe

    from diffusers import DiffusionPipeline

    # TODO: replace with your own checkpoint / repo id
    model_id = "stabilityai/stable-diffusion-xl-base-1.0"
    _pipe = DiffusionPipeline.from_pretrained(model_id, torch_dtype=DTYPE)
    _pipe = _pipe.to(DEVICE)
    return _pipe


def generate(prompt, negative_prompt, steps, guidance_scale, width, height, seed):
    if not prompt or not prompt.strip():
        raise gr.Error("Prompt likh kar daalo pehle.")

    pipe = load_model()

    generator = None
    if seed is not None and int(seed) >= 0:
        generator = torch.Generator(device=DEVICE).manual_seed(int(seed))

    # TODO: replace this call with your DIP AI V-01 generate_image(...) call
    result = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt or None,
        num_inference_steps=int(steps),
        guidance_scale=float(guidance_scale),
        width=int(width),
        height=int(height),
        generator=generator,
    )
    return result.images[0]


with gr.Blocks(title="DIP AI V-01") as demo:
    gr.Markdown(
        """
        # DIP AI V-01
        High quality image generation demo. Prompt daalo aur ultra quality photo banao.
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            prompt = gr.Textbox(
                label="Prompt",
                placeholder="e.g. ultra realistic portrait of a mountain village at sunrise, 8k, sharp focus",
                lines=3,
            )
            negative_prompt = gr.Textbox(
                label="Negative prompt (optional)",
                placeholder="e.g. blurry, low quality, watermark",
                lines=2,
            )

            with gr.Row():
                width = gr.Slider(512, 1536, value=1024, step=64, label="Width")
                height = gr.Slider(512, 1536, value=1024, step=64, label="Height")

            with gr.Row():
                steps = gr.Slider(10, 100, value=30, step=1, label="Steps")
                guidance_scale = gr.Slider(1, 15, value=7.5, step=0.5, label="Guidance scale")

            seed = gr.Number(value=-1, label="Seed (-1 = random)", precision=0)

            generate_btn = gr.Button("Generate", variant="primary")

        with gr.Column(scale=1):
            output_image = gr.Image(label="Result", format="png")

    generate_btn.click(
        fn=generate,
        inputs=[prompt, negative_prompt, steps, guidance_scale, width, height, seed],
        outputs=output_image,
    )

    gr.Examples(
        examples=[
            ["ultra detailed portrait of an old fisherman, golden hour, 8k, sharp focus", "blurry, low quality"],
            ["aerial view of a futuristic city at night, neon lights, ultra high resolution", "blurry, distorted"],
        ],
        inputs=[prompt, negative_prompt],
    )

if __name__ == "__main__":
    demo.queue().launch()

#!/usr/bin/env python

from __future__ import annotations

import gradio as gr
import numpy as np

from model import Model

TITLE = ''
DESCRIPTION = '''# StyleGAN3

This is an unofficial demo for [https://github.com/NVlabs/stylegan3](https://github.com/NVlabs/stylegan3).
'''


def get_sample_image_url(name: str) -> str:
    sample_image_dir = 'https://huggingface.co/spaces/hysts/StyleGAN3/resolve/main/samples'
    return f'{sample_image_dir}/{name}.jpg'


def get_sample_image_markdown(name: str) -> str:
    url = get_sample_image_url(name)
    size = 512 if name == 'afhqv2' else 1024
    seed = '0-99'
    return f'''
    - size: {size}x{size}
    - seed: {seed}
    - truncation: 0.7
    ![sample images]({url})'''


model = Model()

with gr.Blocks(css='style.css') as demo:
    gr.Markdown(DESCRIPTION)

    with gr.Tabs():
        with gr.TabItem('App'):
            with gr.Row():
                with gr.Column():
                    model_name = gr.Dropdown(list(
                        model.MODEL_NAME_DICT.keys()),
                                             value='FFHQ-1024-R',
                                             label='Model')
                    seed = gr.Slider(0,
                                     np.iinfo(np.uint32).max,
                                     step=1,
                                     value=0,
                                     label='Seed')
                    psi = gr.Slider(0,
                                    2,
                                    step=0.05,
                                    value=0.7,
                                    label='Truncation psi')
                    tx = gr.Slider(-1,
                                   1,
                                   step=0.05,
                                   value=0,
                                   label='Translate X')
                    ty = gr.Slider(-1,
                                   1,
                                   step=0.05,
                                   value=0,
                                   label='Translate Y')
                    angle = gr.Slider(-180,
                                      180,
                                      step=5,
                                      value=0,
                                      label='Angle')
                    run_button = gr.Button('Run')
                with gr.Column():
                    result = gr.Image(label='Result', elem_id='result')

        with gr.TabItem('Sample Images'):
            with gr.Row():
                model_name2 = gr.Dropdown([
                    'afhqv2',
                    'ffhq',
                    'ffhq-u',
                    'metfaces',
                    'metfaces-u',
                ],
                                          value='afhqv2',
                                          label='Model')
            with gr.Row():
                text = get_sample_image_markdown(model_name2.value)
                sample_images = gr.Markdown(text)

    model_name.change(fn=model.set_model, inputs=model_name, outputs=None)
    run_button.click(fn=model.set_model_and_generate_image,
                     inputs=[
                         model_name,
                         seed,
                         psi,
                         tx,
                         ty,
                         angle,
                     ],
                     outputs=result)
    model_name2.change(fn=get_sample_image_markdown,
                       inputs=model_name2,
                       outputs=sample_images)

demo.queue().launch(show_api=False)

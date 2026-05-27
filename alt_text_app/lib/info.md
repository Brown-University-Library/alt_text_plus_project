# About the experimental Image Alt-Text Maker

- [Purpose](#purpose)
- [Limitations](#limitations)
- [image alt text](#image-alt-text)
- [this webapp's output](#this-webapps-output)
- [Usage](#usage)

---


## Purpose 

This is an _experimental_ webapp. It serves the following purposes:

- To see if we could use a large-language model (LLM) to give staff and users friendly, useful alt-text suggestions for images.

- To experiment with an "upload and hand-off-to-a-model" architecture because it could be extremely useful for improving the accessibility of a variety of other media.

- To show [OIT][oit] and [CCV][ccv] a working implementation of this architecture -- so we can explore ways we might work with them to use their models for improved privacy, quality, and scalability. 

---


## Limitations

### Privacy

**Don't submit anything you want to keep private.**

When configured for OpenRouter, we send image data to third-party models. If privacy is a concern, avoid uploading sensitive images. When configured for local LM Studio experimentation, image data is sent to the local LM Studio server instead.

Official Brown models offer privacy guarantees that this webapp doesn't.

### Capability

Currently, the production-oriented configuration uses one of the developer's personal [OpenRouter][or] accounts to access a multi-modal model. Local LM Studio can also be used for experimentation with locally loaded vision-capable models. Output quality may vary by selected model.

### Scalability

Due to this personal account, where each request costs a bit of money, we're initially only opening this up to some library-staff, to demo functionality. 

If this proves useful, and we're able to access a Brown model, we'll open this up to the Brown community, and eventually may implement API features on the drawing-board.

_If we're able to work with OIT and CCV to point to official Brown models, we'll note that here. That would address the privacy, capability, and scalability limitations._


---

## Image alt text

Alt text is a concise written description of an image for people who use screen readers or cannot see the image. Good alt text focuses on the most important visual details and avoids extra or redundant phrasing.


---

## this webapp's output

This webapp sends the uploaded image to the configured multimodal model server with a prompt that asks for concise, accessibility-focused alt text.

Here's the [current prompt][prompt]. It will likely change over time as we experiment.

---


## Usage

Typically, you'll select and submit your image file. Usually within 20-seconds, you'll be redirected to the report page. Most of the time, the report page will show suggested alt text at the top.

Copy the url if you want to review or share the report.

If something goes wrong, you'll still be directed to the report page, but it will show a problem with the alt-text suggestion. Still, save that url and try to access it again later. We plan to implement a script to check for temporarily failed jobs and retry them.

Let us know via the feedback link on each page if you have any problems or questions.

---

[ccv]: <https://ccv.brown.edu/>
[oit]: <https://it.brown.edu/>
[or]: <https://openrouter.ai/>
[prompt]: <https://github.com/Brown-University-Library/alt_text_project/blob/main/alt_text_app/lib/prompt.md>

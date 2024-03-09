# RPLorer

Created as assignment submission to [lab administrator recruitment](https://github.com/Lab-RPL-ITS/Modul-Oprec-BE-2024/tree/main)
of Software Engineering Research Lab, Sepuluh Nopember Institute 
of Technology.

```
Name    : Keanu Fortuna Taufan
NRP     : 5025221042
Divison : Backend
```

## What is this?

RPLorer is an API for hypothetical social media app. Requirement
dictates that RPLorer API must implement at least these features:

[x] Register
[x] Login
[x] Create post
[x] Get list of posts made by specific user
[x] Get post details
[x] Like/unlike post
[x] Edit post
[x] Delete post

Participant is free to choose any tech stack to use. In this case,
I experimented with Python web framework [FastAPI](https://github.com/tiangolo/fastapi/).

There are some additions I've made on top of bare minimum requirement
provided:

- User can edit their own profile
- Post can contain user uploaded media (image only for now)
- Media upload is protected with Falcon AI's [NSFW Image Detection](https://huggingface.co/Falconsai/nsfw_image_detection) Deep Learning model

## How to Use

Setup a virtual environment and install of the requirements by
running this command:

```
pip install -r requirements.txt
```

Then, create your own `.env` file based off of `.env.example` provided in app module.

Notes:
- `DB_URL` is PostgreSQL connection string
- `JWT_SECRET` is JWT private key used to issue access token
- `MEDIA_PATH` is directory to host user uploaded file, be sure to exclude it in `.gitignore`
- `FILTERED_MEDIA_PATH` is directory to host filtered image for improving deep learning model
`IMAGE_FILTER_MODEL_PATH` is the path to [NSFW Image Detection](https://huggingface.co/Falconsai/nsfw_image_detection) Deep Learning model


## Docs

FastAPI comes with built in documentation tools. Just go to `{{URL}}/docs`
to see prettified view of the docs or alternatively `{{URL}}/openapi.json`
to see OpenAPI schema.
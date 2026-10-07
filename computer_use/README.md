# Computer use

Claude can use a computer: it looks at screenshots, then moves the mouse and types to complete a task. Anthropic's [quickstart](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) runs this in a Docker container with a Linux desktop (Firefox, a text editor, more), so Claude acts in a sandbox instead of on your Mac.

## Launch

You need Docker running and `ANTHROPIC_API_KEY` exported in your shell (`set -a; source .env; set +a` loads it from the repo's `.env`).

```bash
docker run \
    -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
    -v $HOME/.anthropic:/home/computeruse/.anthropic \
    -p 5900:5900 \
    -p 8501:8501 \
    -p 6080:6080 \
    -p 8080:8080 \
    -it ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo-latest
```

Then open <http://localhost:8080>: the chat is on one side and Claude's desktop on the other. (`8501` is the chat alone, `6080` and `5900` are the desktop in a browser or VNC client.) Stop with `Ctrl+C`.

## Prompts

Type a task in the chat. Step-by-step prompts with an exact file name work best.

```
Open Firefox, go to Wikipedia, and look up the tallest mountain in the world. Then open a text editor, write a short 3-sentence summary of what you found, and save it to the desktop as everest.txt.
```

```
Open Firefox, go to Wikipedia, and look up the longest river in the world. Then open a text editor, write a short 3-sentence summary of what you found, and save it to the desktop as nile.txt.
```

```
Open Firefox, go to Wikipedia, and look up when the Eiffel Tower was completed and how tall it is. Then open a text editor, write a short 3-sentence summary of what you found, and save it to the desktop as eiffel.txt.
```

## Notes

- Files Claude saves stay inside the container. Copy one out while it runs with `docker cp <container>:<path> .` (find the name with `docker ps`).
- Computer use is an API tool you can also drive from your own script. The demo's Python loop is the reference implementation.
- Claude acts on its own and every step is billed to your key. Don't log in to real accounts in the container, and watch what it does.

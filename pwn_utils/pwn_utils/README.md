# pwn_utils

### Running the Dockerfile

Build the Docker image:

```bash
docker build -t hacking .
```

Run the Docker container:

```bash
docker run --rm -ti -v $(pwd):/root/hacking hacking /bin/bash
```

Then run your script using `python3 yourscript.py`

When running the server code for some challenge, be sure to link this directory to your current working directory, such that the import (from pwn_utils import ...) works.

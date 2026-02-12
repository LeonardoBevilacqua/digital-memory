# ollama on nix

use `nix-shell -p ollama` to access the program.
use `ollama serve` to start the serve, doesn't start automatically. without I can get a error like:
`Error: Head "http://127.0.0.1:11434/": dial tcp 127.0.0.1:11434: i/o timeout`

pulling a model `ollama serve & ollama pull <model_name>`

using ollama with phil3:mini


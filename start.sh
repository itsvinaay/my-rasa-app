```bash
#!/bin/bash

echo "Training Rasa model..."
rasa train

echo "Starting Rasa server..."
rasa run --enable-api --cors "*" --debug
```
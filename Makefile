VERSION ?= 1.0.2
MANIFEST := custom_components/hdfury/manifest.json

.PHONY: status bump commit tag push release

status:
	git status --short
	@grep '"version"' $(MANIFEST)

bump:
	python3 - <<'PY'
import json
from pathlib import Path

path = Path("custom_components/hdfury/manifest.json")
data = json.loads(path.read_text())
data["version"] = "$(VERSION)"
path.write_text(json.dumps(data, indent=2) + "\n")
print(f"Updated version to $(VERSION)")
PY

commit: bump
	git add .
	git commit -m "Release v$(VERSION)"

push:
	git push origin main

tag:
	git tag v$(VERSION)
	git push origin v$(VERSION)

release: commit push tag
	@echo "Release v$(VERSION) triggered (GitHub Actions will create it)"

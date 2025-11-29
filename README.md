# Setup
## Configure GitHub Workflows
### `ci.yaml`
Add two variables:
1. `UNIVERSE_ID` : `number`
2. `PLACE_ID` : `number`

Add a secret:
1. `PLACE_PUBLISHING_KEY` : `string`
   * This will be your [api key](https://create.roblox.com/docs/reference/cloud/universes-api/v1).
## Install toolkit manager
Install [Rokit](https://github.com/rojo-rbx/rokit) as your tool manager on your system.
### Rokit
1. Run `rokit update` to update tools before development.

2. Run `rokit install` and agree to trust the tools found in `rokit.toml`.

## Visual Studio Code
Install the recommended extensions found in `extensions.json`

### Configure `Moonwave.toml`
Refer to [Moonwave](https://github.com/evaera/moonwave?tab=readme-ov-file#moonwave)
### Configure `default.project.json`
Refer to Rojo's [Project Format](https://rojo.space/docs/v7/project-format/)

### Setup Lune
1. Run `lune setup` so lune can store its definitions in your home directory

### Setup Asphalt
1. Go into [`asphalt.toml`](asphalt.toml) and edit the `[creator]` properties

2. Store all assets in [`public`](public) directory

3. Get API Key with the [specified permissions](https://github.com/jackTabsCode/asphalt?tab=readme-ov-file#authentication)

4. Run `asphalt sync` in the terminal

# HDFury

[![Release](https://img.shields.io/github/v/release/johncarey70/hdfury-ha)](https://github.com/johncarey70/hdfury-ha/releases)
[![Downloads](https://img.shields.io/github/downloads/johncarey70/hdfury-ha/latest/total)](https://github.com/johncarey70/hdfury-ha/releases)
[![License](https://img.shields.io/github/license/johncarey70/hdfury-ha)](https://github.com/johncarey70/hdfury-ha/blob/main/LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/johncarey70/hdfury-ha)](https://github.com/johncarey70/hdfury-ha/commits/main)

Home Assistant integration for controlling HDFury devices via HTTP.

---

## Features

- Input selection via `select` entity  
- Real-time state tracking (TX0)  
- Fast, direct HTTP control  
- Config Flow (UI setup)  
- Restores last selected value on restart  

---

## Installation (HACS)

1. Open HACS  
2. Go to **Integrations**  
3. Click the menu (three dots) and select **Custom repositories**  
4. Add this repository  
5. Select category **Integration**  
6. Install **HDFury**  
7. Restart Home Assistant  

---

## Configuration

1. Go to **Settings > Devices & Services**  
2. Click **Add Integration**  
3. Search for **HDFury**  

Enter:

- **Name** - Friendly name  
- **Host** - Device IP (e.g. `192.168.15.33`)  

---

## Entities

### Input Select

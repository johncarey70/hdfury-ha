# HDFury

![Release](https://img.shields.io/github/v/release/johncarey70/hdfury-ha)
![Downloads](https://img.shields.io/github/downloads/johncarey70/hdfury-ha/latest/total)
![License](https://img.shields.io/github/license/johncarey70/hdfury-ha)
![Last Commit](https://img.shields.io/github/last-commit/johncarey70/hdfury-ha)

Home Assistant custom integration for controlling HDFury devices via HTTP.

---

## Features

- Input selection via `select` entity  
- Fast, direct HTTP control  
- Config Flow (UI setup)  
- Restores last selected value on restart  

---

## Installation (HACS)

1. Open HACS  
2. Go to **Integrations**  
3. Click **? ? Custom repositories**  
4. Add this repository  
5. Select category **Integration**  
6. Install **HDFury**  
7. Restart Home Assistant  

---

## Configuration

1. Go to **Settings ? Devices & Services**  
2. Click **Add Integration**  
3. Search for **HDFury**  
4. Enter:
   - **Name**  Friendly name  
   - **Host**  Device IP (e.g. `192.168.15.33`)  

---

## Entities

### Input Select

```
select.<name>_input
```

Options:

- Input 0  
- Input 1  
- Input 2  
- Input 3  

---

## Behavior

Each selection sends:

```
http://<host>/cmd?insel0
http://<host>/cmd?insel1
http://<host>/cmd?insel2
http://<host>/cmd?insel3
```

- Optimistic updates (no polling)  
- Immediate UI response  
- Last value restored on restart  

---

## Limitations

- No state feedback from device  
- Assumes commands succeed  
- Requires reachable HTTP interface  

---

## License

MIT

---

## Notes

- Repo: `hdfury-ha`  
- Integration domain: `hdfury`  
- Designed for expansion (additional entities and features can be added later)  

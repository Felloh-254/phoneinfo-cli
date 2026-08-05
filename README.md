# phoneinfo-cli

A simple terminal tool to look up info about a phone number: validity, country,
carrier, timezone, and line type. Works from any directory, just like any
other terminal command.

## Install

```bash
git clone https://github.com/Felloh-254/phoneinfo-cli.git
cd phoneinfo-cli
pipx install .
```

Don't have `pipx`? Install it first:

```bash
sudo apt install pipx
pipx ensurepath
```

Then restart your terminal (or run `source ~/.bashrc`) and repeat the install step above.

That's it. `phoneinfo` is now available anywhere in your terminal.

## Usage

```bash
phoneinfo +260972693740
```

```
Number:        +260972693740
Formatted:     +260 97 2693740
Valid number:  True
Country:       Zambia
Carrier:       Airtel
Timezone:      Africa/Lusaka
Type:          Mobile
```

If your number doesn't include a country code, pass a region:

```bash
phoneinfo 0972693740 --region ZM
```

## Update

```bash
cd phoneinfo-cli
git pull
pipx install . --force
```

## Uninstall

```bash
pipx uninstall phoneinfo-cli
```

## License

MIT — see [LICENSE](LICENSE)

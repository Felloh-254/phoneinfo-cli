# phoneinfo-cli

A simple terminal tool to look up info about a phone number: validity, country,
carrier, timezone, and line type.

## Install

Directly from GitHub (no need to clone manually):

```bash
pip install git+https://github.com/YOUR_USERNAME/phoneinfo-cli.git
```

Or, if you've cloned it locally:

```bash
git clone https://github.com/YOUR_USERNAME/phoneinfo-cli.git
cd phoneinfo-cli
pip install .
```

Either way, this installs a `phoneinfo` command onto your PATH.

## Usage

```bash
phoneinfo +260972693740
```

The `+` is optional as long as the country code is included:

```bash
phoneinfo 260972693740
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

If your number is in local format (no country code at all), pass a region:

```bash
phoneinfo 0972693740 --region ZM
```

## Updating

```bash
pip install --upgrade git+https://github.com/YOUR_USERNAME/phoneinfo-cli.git
```

## Uninstall

```bash
pip uninstall phoneinfo-cli
```

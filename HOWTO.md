# Versuchsumgebung

## 1. Virtual Box herunterladen

Als erstes natürlich Virtual Box herunterladen und installieren, falls noch nicht geschehen.

https://www.virtualbox.org/wiki/Downloads

Wir haben die Version `7.0.0 r153978 (Qt5.15.2)` verwendet.

## 2. Kali Linux herunterladen

Als nächstes das Kali Linux ISO Image herunterladen.

https://www.kali.org/get-kali/#kali-installer-images

Wir haben Version `2022.3` verwendet. Die aktuelle Version ist `2022.4`, die aber wahrscheinlich genauso funktionieren sollte.

## 3. Virtuelle Maschinen aufsetzen

Als nächstes müssen 2 virtuelle Maschinen in VirtualBox angelegt werden:

- Kali 2022.4 Client
- Kali 2022.4 Server

Folgende Konfiguration der beiden VMs haben wir verwendet und getestet:

Name | Wert
--- | ---
CPU | 4 Kerne
RAM | 4096 MB
Festplatte | 20 GB (dynamisch)
Netzwerk | Netzwerkbrücke
Grafikspeicher | 128 MB

Jeweils Kali Linux ISO auswählen und ganz normal installieren.

## 4. Software installieren

### Pakete updaten

Zuerst Pakete updaten:

```sh
sudo apt update
sudo apt upgrade
```

### ProSys OPC UA Simulation Server / Browser

Prosys OPC UA Simulation Server / Browser auf Server / Client VM installieren:

Simulation Server: https://downloads.prosysopc.com/opc-ua-simulation-server-downloads.php

Browser: https://downloads.prosysopc.com/opc-ua-browser-downloads.php

### Nfqueue installieren

Pakete installieren:

```sh
sudo apt install build-essential python-dev libnetfilter-queue-dev
```

Python-Modul installieren:

```sh
pip install NetfilterQueue
```

Siehe auch: https://github.com/oremanj/python-netfilterqueue

### Git Repository clonen

```sh
git clone https://github.com/azmke/opcua
```
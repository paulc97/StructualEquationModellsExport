# Structural Equation Models Export

Dieses Projekt wurde im Rahmen meiner Bachelorarbeit entwickelt und bietet eine Anwendung zur automatischen Extraktion und Klassifizierung von Bildern aus PDF-Dokumenten, insbesondere von Strukturgleichungsmodellen.

## Inhaltsverzeichnis

- [Über das Projekt](#über-das-projekt)
- [Funktionen](#funktionen)
- [Voraussetzungen](#voraussetzungen)
- [Installation](#installation)
- [Nutzung](#nutzung)
- [Projektstruktur](#projektstruktur)
- [Technologien](#technologien)
- [Hinweise](#hinweise)
- [Kontakt](#kontakt)

## Über das Projekt

Die Anwendung ermöglicht es, PDF-Dokumente hochzuladen, aus denen automatisch Bilder extrahiert werden. Anschließend werden diese Bilder mithilfe eines vortrainierten neuronalen Netzes analysiert und klassifiziert. Das Hauptziel ist die Identifikation und Verarbeitung von Strukturgleichungsmodellen in wissenschaftlichen Publikationen.

## Funktionen

- **PDF-Upload**: Laden Sie ein PDF-Dokument über die Weboberfläche hoch.
- **Bildextraktion**: Automatische Extraktion aller Bilder aus dem hochgeladenen PDF.
- **Bildklassifizierung**: Analyse der extrahierten Bilder mittels eines vortrainierten neuronalen Netzes.
- **Ergebnisse anzeigen**: Visualisierung der Ergebnisse mit Wahrscheinlichkeitseinschätzungen.
- **Download**: Möglichkeit, die klassifizierten Bilder herunterzuladen.

## Voraussetzungen

- **Docker** und **Git** müssen auf Ihrem Host-System installiert sein.

Falls diese Tools noch nicht installiert sind, folgen Sie bitte der offiziellen [Docker-Installationsanleitung](https://docs.docker.com/get-docker/) und [Git-Installationsanleitung](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

## Installation

Folgen Sie diesen Schritten, um die Anwendung auf Ihrem Docker-Host zu installieren und zu starten.

### 1. Repository klonen

Klonen Sie das GitHub-Repository auf Ihren Docker-Host:

```bash
git clone https://github.com/paulc97/StructualEquationModellsExport.git
cd StructualEquationModellsExport
```

### 2. Anwendung starten

Starten Sie die Anwendung mit Docker Compose:

```bash
docker-compose up -d --build
```

Dieser Befehl erstellt die notwendigen Docker-Images und startet die Dienste im Hintergrund.

### 3. Anwendung aufrufen

Öffnen Sie einen Webbrowser und navigieren Sie zu: http://Ihre-Docker-Host-IP:80

## Nutzung

1. **Weboberfläche öffnen**: Besuchen Sie die Anwendung im Browser.
2. **PDF hochladen**: Klicken Sie auf "Datei auswählen" und wählen Sie ein PDF-Dokument aus.
3. **Analyse starten**: Laden Sie die Datei hoch, um die Verarbeitung zu starten.
4. **Ergebnisse ansehen**: Nach der Analyse werden die Ergebnisse angezeigt, einschließlich der Wahrscheinlichkeitseinschätzungen für jedes Bild.
5. **Bilder herunterladen**: Sie können die klassifizierten Bilder einzeln herunterladen.

## Projektstruktur

- **frontend/**: Enthält den Angular-Frontend-Code.
- **backend/**: Enthält den Flask-Backend-Code.
- **docker-compose.yml**: Docker Compose Datei zum Orchestrieren der Container.
- **README.md**: Dokumentation des Projekts.

## Technologien

- **Frontend**:
  - Angular
  - Nginx (als Webserver und Reverse Proxy)

- **Backend**:
  - Python
  - Flask
  - PyTorch (für das vortrainierte Modell)
  - Weitere Python-Bibliotheken (siehe `backend/requirements.txt`)

- **Containerisierung**:
  - Docker
  - Docker Compose

## Hinweise

- **Sicherheit**: Stellen Sie sicher, dass der Docker-Host und die Anwendung entsprechend abgesichert sind, insbesondere wenn sie öffentlich zugänglich gemacht werden.
- **Leistung**: Die Verarbeitung großer PDF-Dateien oder einer großen Anzahl von Bildern kann ressourcenintensiv sein.
- **Erweiterbarkeit**: Das Projekt kann erweitert werden, um zusätzliche Funktionen oder Anpassungen am Modell vorzunehmen.

## Kontakt

Bei Fragen oder Anmerkungen können Sie mich gerne kontaktieren:

- **Name**: Paul Czichos.
- **E-Mail**: paul@czichos.net





import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
  selectedFile: File | null = null;
  fileUrl: SafeResourceUrl | null = null;
  responseData: any[] | null = null;

  positiveResponses: any[] = [];
  negativeResponses: any[] = [];

  isPositiveExpanded = true;
  isNegativeExpanded = false;

  constructor(private sanitizer: DomSanitizer) {}

  onClickUpload() {
    const upload = document.getElementById('upload') as HTMLInputElement;
    upload?.click();
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
      this.fileUrl = this.sanitizer.bypassSecurityTrustResourceUrl(
        URL.createObjectURL(this.selectedFile)
      );
      console.log('Ausgewählte Datei:', this.selectedFile);
    }
  }

  uploadFile() {
    if (this.selectedFile) {
      const formData = new FormData();
      formData.append('file', this.selectedFile);

      fetch('/process_pdf', {
        method: 'POST',
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          console.log('Datei erfolgreich hochgeladen', data);
          this.responseData = data;

          this.positiveResponses = data.filter(
            (item: any) => item.probability_positive > 0.75
          );
          this.negativeResponses = data.filter(
            (item: any) => item.probability_positive <= 0.75
          );

          this.positiveResponses.sort(
            (a: any, b: any) => b.probability_positive - a.probability_positive
          );
          this.negativeResponses.sort(
            (a: any, b: any) => b.probability_positive - a.probability_positive
          );

          this.selectedFile = null;
          this.fileUrl = null;
        })
        .catch((error) => {
          console.error('Fehler:', error);
        });
    }
  }

  togglePositive() {
    this.isPositiveExpanded = !this.isPositiveExpanded;
  }

  toggleNegative() {
    this.isNegativeExpanded = !this.isNegativeExpanded;
  }

  sanitizeImage(base64: string): SafeResourceUrl {
    return this.sanitizer.bypassSecurityTrustResourceUrl(
      `data:image/png;base64,${base64}`
    );
  }

  downloadImage(item: any) {
    const link = document.createElement('a');
    link.href = `data:image/png;base64,${item.image}`;
    link.download = item.name;
    link.click();
  }

  reset() {
    this.selectedFile = null;
    this.fileUrl = null;
    this.responseData = null;
    this.positiveResponses = [];
    this.negativeResponses = [];
    this.isPositiveExpanded = true;
    this.isNegativeExpanded = false;
  }

  roundToFourDecimals(percentage: any) {
    return Math.round(percentage * 10000) / 100;
  }
}

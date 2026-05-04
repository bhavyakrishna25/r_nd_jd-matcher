import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';

import { AnalysisService } from '../../services/analysis.service';

@Component({
  selector: 'app-upload-resume',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './upload-resume.component.html',
  styleUrl: './upload-resume.component.css'
})
export class UploadResumeComponent {
  readonly analysisService = inject(AnalysisService);
  readonly acceptedFileTypes = '.pdf,.docx';

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0] ?? null;
    this.analysisService.setResumeFile(file);
  }
}

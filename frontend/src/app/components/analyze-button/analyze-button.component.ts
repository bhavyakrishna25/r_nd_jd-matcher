import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';

import { AnalysisService } from '../../services/analysis.service';

@Component({
  selector: 'app-analyze-button',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './analyze-button.component.html',
  styleUrl: './analyze-button.component.css'
})
export class AnalyzeButtonComponent {
  readonly analysisService = inject(AnalysisService);

  onAnalyze(): void {
    this.analysisService.analyzeResume();
  }
}

import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';

import { CriteriaBreakdownItem } from '../../models/analysis-result.model';
import { AnalysisService } from '../../services/analysis.service';

@Component({
  selector: 'app-results',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './results.component.html',
  styleUrl: './results.component.css'
})
export class ResultsComponent {
  readonly analysisService = inject(AnalysisService);

  trackByValue(_: number, value: string | CriteriaBreakdownItem): string {
    return typeof value === 'string' ? value : value.criterion;
  }
}

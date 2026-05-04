import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { AnalysisService } from '../../services/analysis.service';

@Component({
  selector: 'app-job-description',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './job-description.component.html',
  styleUrl: './job-description.component.css'
})
export class JobDescriptionComponent {
  readonly analysisService = inject(AnalysisService);

  onJobDescriptionChange(value: string): void {
    this.analysisService.setJobDescription(value);
  }
}

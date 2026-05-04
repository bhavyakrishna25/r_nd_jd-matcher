import { Component } from '@angular/core';

import { AnalyzeButtonComponent } from './components/analyze-button/analyze-button.component';
import { JobDescriptionComponent } from './components/job-description/job-description.component';
import { ResultsComponent } from './components/results/results.component';
import { UploadResumeComponent } from './components/upload-resume/upload-resume.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    UploadResumeComponent,
    JobDescriptionComponent,
    AnalyzeButtonComponent,
    ResultsComponent
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'AI Resume Matcher';
}

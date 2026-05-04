import { HttpClient } from '@angular/common/http';
import { Injectable, computed, inject, signal } from '@angular/core';

import { AnalysisResult } from '../models/analysis-result.model';

@Injectable({
  providedIn: 'root'
})
export class AnalysisService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = 'http://127.0.0.1:8000';

  readonly selectedFile = signal<File | null>(null);
  readonly jobDescription = signal('');
  readonly result = signal<AnalysisResult | null>(null);
  readonly loading = signal(false);
  readonly errorMessage = signal('');

  readonly canAnalyze = computed(() => {
    return !!this.selectedFile() && this.jobDescription().trim().length > 0 && !this.loading();
  });

  setResumeFile(file: File | null): void {
    this.selectedFile.set(file);
    this.errorMessage.set('');
  }

  setJobDescription(value: string): void {
    this.jobDescription.set(value);
    this.errorMessage.set('');
  }

  analyzeResume(): void {
    const file = this.selectedFile();
    const jobDescription = this.jobDescription().trim();

    if (!file) {
      this.errorMessage.set('Please upload a resume.');
      return;
    }

    if (!jobDescription) {
      this.errorMessage.set('Enter job description.');
      return;
    }

    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_description', jobDescription);

    this.loading.set(true);
    this.errorMessage.set('');
    this.result.set(null);

    this.http.post<AnalysisResult>(`${this.apiUrl}/analyze`, formData).subscribe({
      next: (response) => {
        this.result.set(response);
        this.loading.set(false);
      },
      error: (error) => {
        const fallbackMessage = 'Failed to analyze resume. Please try again.';
        const detail = error?.error?.detail;
        this.errorMessage.set(typeof detail === 'string' ? detail : fallbackMessage);
        this.loading.set(false);
      }
    });
  }
}

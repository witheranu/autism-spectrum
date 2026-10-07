import { BenchmarkEntry, ClassifierResult, Conversation } from './types';
import conversationsData from '../data/mock/conversations.json';
import classifierResultsData from '../data/mock/classifier_results.json';
import benchmarkResultsData from '../data/mock/benchmark_results.json';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function getConversations(): Promise<Conversation[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/conversations`, { cache: 'no-store' });
    if (!res.ok) {
      return conversationsData as Conversation[];
    }
    const data = await res.json();
    return data.length > 0 ? data : (conversationsData as Conversation[]);
  } catch {
    return conversationsData as Conversation[];
  }
}

export async function getConversation(id: string): Promise<Conversation | undefined> {
  try {
    const res = await fetch(`${API_BASE_URL}/conversations/${id}`, { cache: 'no-store' });
    if (!res.ok) {
      return (conversationsData as Conversation[]).find((c) => c.id === id);
    }
    return await res.json();
  } catch {
    return (conversationsData as Conversation[]).find((c) => c.id === id);
  }
}

export async function getClassifierResults(): Promise<ClassifierResult[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/classifier/results`, { cache: 'no-store' });
    if (!res.ok) {
      return classifierResultsData as ClassifierResult[];
    }
    const data = await res.json();
    return data.length > 0 ? data : (classifierResultsData as ClassifierResult[]);
  } catch {
    return classifierResultsData as ClassifierResult[];
  }
}

export async function getBenchmarkResults(): Promise<BenchmarkEntry[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/bias/benchmark`, { cache: 'no-store' });
    if (!res.ok) {
      return benchmarkResultsData as BenchmarkEntry[];
    }
    const data = await res.json();
    return data.length > 0 ? data : (benchmarkResultsData as BenchmarkEntry[]);
  } catch {
    return benchmarkResultsData as BenchmarkEntry[];
  }
}

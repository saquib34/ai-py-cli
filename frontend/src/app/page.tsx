import Terminal from '@/components/Terminal';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-900 p-4">
      <div className="max-w-6xl mx-auto">
        <div className="mb-4 text-center">
          <h1 className="text-2xl font-bold text-green-400 mb-2">
            🤖 AI Terminal - Web Interface
          </h1>
          <p className="text-gray-400 text-sm">
            Intelligent command line with AI assistance and system monitoring
          </p>
        </div>
        <Terminal />
      </div>
    </div>
  );
}

import React, { useState } from 'react';
import { Upload, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';
import { Button } from '../components/ui/button';

const DisasterIdentifier = () => {
  const [tweetResult, setTweetResult] = useState<'true' | 'false' | null>(null);
  const [imageResult, setImageResult] = useState<{
    severity: 'Low' | 'Medium' | 'High' | null;
    type: string | null;
  }>({ severity: null, type: null });

  const analyzeTweet = async () => {
    const tweetText = (document.querySelector("textarea") as HTMLTextAreaElement).value;
  
    if (!tweetText.trim()) {
      alert("Please enter a tweet for analysis.");
      return;
    }
  
    try {
      const response = await fetch("http://127.0.0.1:5000/analyze-tweet", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tweet: tweetText }),
      });
  
      const data = await response.json();
  
      if (response.ok) {
        setTweetResult(data.result);
      } else {
        alert("Error: " + (data.error || "Could not analyze tweet"));
      }
    } catch (error) {
      alert("Failed to connect to server. Is Flask running?");
    }
  };
  

  const [imageFile, setImageFile] = useState<File | null>(null);

const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
  const file = event.target.files?.[0];
  if (file) {
    setImageFile(file);
  }
};

const analyzeImage = async () => {
  if (!imageFile) {
    alert("Please upload an image first.");
    return;
  }

  const formData = new FormData();
  formData.append("image", imageFile);

  try {
    const response = await fetch("http://127.0.0.1:5000/analyze-image", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (response.ok) {
      setImageResult({ severity: data.severity, type: data.type });
    } else {
      alert("Error: " + (data.error || "Could not analyze image"));
    }
  } catch (error) {
    alert("Failed to connect to server. Is Flask running?");
  }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-red-500 to-orange-500 mb-4">
            Disaster Identifier
          </h1>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Advanced AI-powered disaster detection and classification system
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-gray-800/50 backdrop-blur-sm p-6 rounded-xl border border-gray-700">
            <div className="flex items-center mb-4">
              <AlertTriangle className="h-6 w-6 text-orange-500 mr-2" />
              <h2 className="text-xl font-semibold">Tweet Analysis</h2>
            </div>
            <div className="space-y-4">
              <textarea
                className="w-full h-32 p-4 rounded-lg bg-gray-700/50 border border-gray-600 focus:outline-none focus:border-orange-500 text-gray-200 placeholder-gray-400"
                placeholder="Enter tweet text for disaster analysis..."
              />
              <Button
                onClick={analyzeTweet}
                className="w-full bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600"
              >
                Analyze Tweet
              </Button>
              {tweetResult !== null && (
                <div className={`flex items-center p-4 rounded-lg ${
                  tweetResult === 'true' ? 'bg-green-500/20' : 'bg-red-500/20'
                }`}>
                  {tweetResult === 'true' ? (
                    <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
                  ) : (
                    <XCircle className="h-5 w-5 text-red-500 mr-2" />
                  )}
                  <span>
                    This tweet is {tweetResult === 'true' ? 'a real' : 'a false'} disaster alert
                  </span>
                </div>
              )}
            </div>
          </div>

          <div className="bg-gray-800/50 backdrop-blur-sm p-6 rounded-xl border border-gray-700">
            <div className="flex items-center mb-4">
              <Upload className="h-6 w-6 text-blue-500 mr-2" />
              <h2 className="text-xl font-semibold">CCTV Image Analysis</h2>
            </div>
            <div className="space-y-4">
              {/* ✅ CHANGE: Hidden File Input for Selecting Images */}
              <input 
                type="file" 
                accept="image/*" 
                id="fileUpload" 
                className="hidden" 
                onChange={handleFileChange} // ✅ CHANGE: Calls function to store selected file
              />
              <div
                className="border-2 border-dashed border-gray-600 rounded-lg p-8 text-center hover:border-blue-500 transition-colors cursor-pointer"
                onClick={() => document.getElementById("fileUpload")?.click()}
              >
                <Upload className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                <p className="text-gray-400">
                {imageFile ? `Selected: ${imageFile.name}` : "Drop CCTV images here or click to upload"}
                </p>
              </div>
              <Button
                onClick={analyzeImage}
                className="w-full bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600"
              >
              Analyze Image
              </Button>
              {imageResult.severity && (
                <div className="space-y-2 p-4 rounded-lg bg-blue-500/20">
                  <div className="flex items-center">
                    <span className="font-semibold mr-2">Severity:</span>
                    <span className={`px-2 py-1 rounded ${
                      imageResult.severity === 'High' ? 'bg-red-500/50' :
                      imageResult.severity === 'Medium' ? 'bg-orange-500/50' :
                      'bg-green-500/50'
                    }`}>
                      {imageResult.severity}
                    </span>
                  </div>
                  <div className="flex items-center">
                    <span className="font-semibold mr-2">Type:</span>
                    <span>{imageResult.type}</span>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DisasterIdentifier;
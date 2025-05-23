import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { UploadCloud, FileUp, File, Trash2, CheckCircle2, X, Loader2 } from "lucide-react";
import { useState, Dispatch, SetStateAction } from "react";
import { toast } from "sonner";

type FileStatus = "idle" | "uploading" | "processing" | "complete" | "error";

type UploadedFile = {
  id: string;
  name: string;
  size: number;
  progress: number;
  status: FileStatus;
  error?: string;
};

const API_URL = "http://localhost:8000";

type UploadPanelProps = {
  onAnalysis?: (analysis: any) => void;
};

export function UploadPanel({ onAnalysis }: UploadPanelProps) {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = async (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    console.log("Drop event triggered", e.dataTransfer.files);
    if (e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      await uploadFile(file);
    }
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log("File input changed", e.target.files);
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      await uploadFile(file);
    }
  };

  const uploadFile = async (file: File) => {
    console.log("Uploading file...", file);
    // Validate file type
    const allowedTypes = ['.pdf', '.doc', '.docx'];
    const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    if (!allowedTypes.includes(fileExtension)) {
      toast.error('Invalid file type. Please upload a PDF or Word document.');
      return;
    }

    // Validate file size (25MB limit)
    if (file.size > 25 * 1024 * 1024) {
      toast.error('File size exceeds 25MB limit.');
      return;
    }

    const newFile: UploadedFile = {
      id: `file-${Date.now()}`,
      name: file.name,
      size: file.size,
      progress: 0,
      status: "uploading",
    };
    setFiles(prev => [...prev, newFile]);
    setIsUploading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);
      console.log("Sending fetch to backend...", `${API_URL}/analyze/document`);
      const response = await fetch(`${API_URL}/analyze/document`, {
        method: 'POST',
        body: formData,
      });
      console.log("Fetch sent, waiting for response...");
      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }
      const result = await response.json();
      console.log("Backend response received:", result);
      if (onAnalysis && result && result.results) {
        onAnalysis(result.results);
      }
      setFiles(prev => 
        prev.map(f => 
          f.id === newFile.id 
            ? { ...f, status: "complete", progress: 100 } 
            : f
        )
      );
      toast.success('Document uploaded and analyzed successfully!');
    } catch (error) {
      console.error('Upload error:', error);
      setFiles(prev => 
        prev.map(f => 
          f.id === newFile.id 
            ? { ...f, status: "error", error: error.message } 
            : f
        )
      );
      toast.error('Failed to upload document. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  const removeFile = (id: string) => {
    setFiles(files.filter(file => file.id !== id));
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' bytes';
    else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    else return (bytes / 1048576).toFixed(1) + ' MB';
  };

  const getStatusIcon = (status: FileStatus) => {
    switch (status) {
      case "uploading": return <div className="h-5 w-5 rounded-full border-2 border-blue-500 border-t-transparent animate-spin" />;
      case "processing": return <Loader2 className="h-5 w-5 text-blue-500 animate-spin" />;
      case "complete": return <CheckCircle2 className="h-5 w-5 text-green-500" />;
      case "error": return <X className="h-5 w-5 text-red-500" />;
      default: return null;
    }
  };
  
  return (
    <div className="flex flex-col gap-6">
      <Card className="glass-panel">
        <CardHeader>
          <CardTitle>Upload Documents</CardTitle>
          <CardDescription>
            Upload legal documents for AI-powered analysis
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div
            className={`border-2 border-dashed rounded-lg p-6 ${
              isDragging 
                ? "border-primary bg-primary/5" 
                : "border-muted hover:border-muted-foreground/50"
            } transition-colors duration-200 text-center cursor-pointer`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => document.getElementById("file-upload")?.click()}
          >
            <input
              id="file-upload"
              type="file"
              className="hidden"
              onChange={handleFileChange}
              accept=".pdf,.doc,.docx"
            />
            <div className="flex flex-col items-center justify-center space-y-4">
              <div className="rounded-full p-3 bg-primary/10">
                <UploadCloud className="h-8 w-8 text-primary" />
              </div>
              <div className="space-y-1 text-center">
                <p className="text-sm font-medium">
                  <span className="text-primary">Click to upload</span> or drag and drop
                </p>
                <p className="text-xs text-muted-foreground">
                  PDF, Word documents up to 25MB
                </p>
              </div>
            </div>
          </div>
        </CardContent>
        <CardFooter>
          <div className="flex justify-between w-full text-xs text-muted-foreground">
            <span>Supported formats: PDF, DOCX, DOC</span>
            <span>Max size: 25MB</span>
          </div>
        </CardFooter>
      </Card>

      {files.length > 0 && (
        <Card className="glass-panel">
          <CardHeader>
            <CardTitle>Document Library</CardTitle>
            <CardDescription>
              Your uploaded legal documents
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {files.map((file) => (
                <div
                  key={file.id}
                  className="flex items-center justify-between p-3 bg-background/60 rounded-lg hover-scale"
                >
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded-md bg-primary/10">
                      <File className="h-5 w-5 text-primary" />
                    </div>
                    <div>
                      <p className="text-sm font-medium">{file.name}</p>
                      <p className="text-xs text-muted-foreground">
                        {formatFileSize(file.size)}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="flex items-center">
                      {getStatusIcon(file.status)}
                      <span className="ml-2 text-xs capitalize">
                        {file.status === "uploading" ? `${file.progress}%` : file.status}
                      </span>
                    </div>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => removeFile(file.id)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
          <CardFooter>
            <div className="flex justify-between w-full">
              <span className="text-xs text-muted-foreground">
                {files.length} document{files.length !== 1 ? "s" : ""}
              </span>
              <Button
                variant="outline"
                size="sm"
                className="text-xs"
                onClick={() => setFiles([])}
              >
                Clear All
              </Button>
            </div>
          </CardFooter>
        </Card>
      )}
    </div>
  );
}

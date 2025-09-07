// Jitsi Meet integration service using IFrame API
// Documentation: https://jitsi.github.io/handbook/docs/dev-guide/dev-guide-iframe

interface JitsiMeetConfig {
  roomName: string;
  displayName: string;
  email?: string;
  avatarUrl?: string;
  subject?: string;
}

interface JitsiMeetOptions {
  roomName: string;
  width?: string | number;
  height?: string | number;
  parentNode?: HTMLElement;
  configOverwrite?: Record<string, any>;
  interfaceConfigOverwrite?: Record<string, any>;
  jwt?: string;
  onload?: () => void;
  invitees?: Array<{ id: string; avatar: string; name: string; }>;
  devices?: {
    audioInput?: string;
    audioOutput?: string;
    videoInput?: string;
  };
  userInfo?: {
    displayName?: string;
    email?: string;
  };
}

declare global {
  interface Window {
    JitsiMeetExternalAPI: any;
  }
}

class JitsiService {
  private api: any = null;
  private isScriptLoaded = false;

  // Load Jitsi Meet External API script
  async loadJitsiScript(): Promise<void> {
    if (this.isScriptLoaded) return;

    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = 'https://meet.jit.si/external_api.js';
      script.async = true;
      script.onload = () => {
        this.isScriptLoaded = true;
        resolve();
      };
      script.onerror = () => reject(new Error('Failed to load Jitsi script'));
      document.head.appendChild(script);
    });
  }

  // Initialize Jitsi Meet conference
  async initializeConference(config: JitsiMeetConfig, containerId: string): Promise<any> {
    try {
      await this.loadJitsiScript();
      
      const container = document.getElementById(containerId);
      if (!container) {
        throw new Error(`Container with id ${containerId} not found`);
      }

      const options: JitsiMeetOptions = {
        roomName: config.roomName,
        width: '100%',
        height: '500px',
        parentNode: container,
        configOverwrite: {
          prejoinPageEnabled: false,
          startWithAudioMuted: true,
          startWithVideoMuted: false,
          enableWelcomePage: false,
          enableClosePage: false,
        },
        interfaceConfigOverwrite: {
          TOOLBAR_BUTTONS: [
            'microphone', 'camera', 'closedcaptions', 'desktop', 'fullscreen',
            'fodeviceselection', 'hangup', 'profile', 'chat', 'recording',
            'livestreaming', 'etherpad', 'sharedvideo', 'settings', 'raisehand',
            'videoquality', 'filmstrip', 'invite', 'feedback', 'stats', 'shortcuts',
            'tileview', 'videobackgroundblur', 'download', 'help', 'mute-everyone'
          ]
        },
        userInfo: {
          displayName: config.displayName,
          email: config.email
        }
      };

      if (config.subject) {
        options.configOverwrite = {
          ...options.configOverwrite,
          subject: config.subject
        };
      }

      this.api = new window.JitsiMeetExternalAPI('meet.jit.si', options);
      
      return this.api;
    } catch (error) {
      console.error('Failed to initialize Jitsi conference:', error);
      throw error;
    }
  }

  // Event handlers
  onReadyToClose(callback: () => void): void {
    if (this.api) {
      this.api.addEventListener('readyToClose', callback);
    }
  }

  onParticipantJoined(callback: (participant: any) => void): void {
    if (this.api) {
      this.api.addEventListener('participantJoined', callback);
    }
  }

  onParticipantLeft(callback: (participant: any) => void): void {
    if (this.api) {
      this.api.addEventListener('participantLeft', callback);
    }
  }

  onVideoConferenceJoined(callback: (participant: any) => void): void {
    if (this.api) {
      this.api.addEventListener('videoConferenceJoined', callback);
    }
  }

  onVideoConferenceLeft(callback: () => void): void {
    if (this.api) {
      this.api.addEventListener('videoConferenceLeft', callback);
    }
  }

  // Control methods
  executeCommand(command: string, ...args: any[]): void {
    if (this.api) {
      this.api.executeCommand(command, ...args);
    }
  }

  hangup(): void {
    if (this.api) {
      this.api.executeCommand('hangup');
    }
  }

  toggleAudio(): void {
    if (this.api) {
      this.api.executeCommand('toggleAudio');
    }
  }

  toggleVideo(): void {
    if (this.api) {
      this.api.executeCommand('toggleVideo');
    }
  }

  // Cleanup
  dispose(): void {
    if (this.api) {
      this.api.dispose();
      this.api = null;
    }
  }

  // Generate room names
  static generateRoomName(circleId: string, sessionId?: string): string {
    const base = `inquirycircle-${circleId}`;
    return sessionId ? `${base}-${sessionId}` : base;
  }
}

const jitsiService = new JitsiService();

export default jitsiService;
export { JitsiService };
export type { JitsiMeetConfig };
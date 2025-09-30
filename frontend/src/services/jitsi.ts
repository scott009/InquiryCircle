// Jitsi Meet integration service using IFrame API
// Documentation: https://jitsi.github.io/handbook/docs/dev-guide/dev-guide-iframe

interface JitsiMeetConfig {
  roomName: string;
  displayName: string;
  email?: string;
  avatarUrl?: string;
  subject?: string;
  password?: string;
  moderator?: boolean;
  jwt?: string;
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
  private currentRoom: string | null = null;
  private jitsiDomain = 'meet.jit.si'; // Can be configured for custom domains

  // Configure Jitsi domain (for custom instances)
  setJitsiDomain(domain: string): void {
    this.jitsiDomain = domain;
    this.isScriptLoaded = false; // Force reload script from new domain
  }

  // Load Jitsi Meet External API script
  async loadJitsiScript(): Promise<void> {
    if (this.isScriptLoaded) return;

    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = `https://${this.jitsiDomain}/external_api.js`;
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
        jwt: config.jwt, // JWT token for authentication
        configOverwrite: {
          prejoinPageEnabled: false,
          startWithAudioMuted: true,
          startWithVideoMuted: false,
          enableWelcomePage: false,
          enableClosePage: false,
          disableInviteFunctions: true,
          enableLobbyChat: false,
          enableInsecureRoomNameWarning: false,
          // Disable authentication and security features
          enableUserRolesBasedOnToken: false,
          disableModeratorIndicator: false,
          requireDisplayName: false,
          enableNoisyMicDetection: false,
          // Room security settings
          ...(config.password && {
            roomPassword: config.password
          })
        },
        interfaceConfigOverwrite: {
          // Simplified toolbar for inquiry circles
          TOOLBAR_BUTTONS: [
            'microphone', 'camera', 'desktop', 'fullscreen',
            'hangup', 'chat', 'raisehand', 'tileview',
            ...(config.moderator ? ['mute-everyone', 'invite'] : [])
          ],
          SHOW_JITSI_WATERMARK: false,
          SHOW_WATERMARK_FOR_GUESTS: false,
          SHOW_BRAND_WATERMARK: false,
          BRAND_WATERMARK_LINK: '',
          DEFAULT_BACKGROUND: '#1e3a8a', // Blue background
          DISABLE_VIDEO_BACKGROUND: false,
          SHOW_PROMOTIONAL_CLOSE_PAGE: false,
          SHOW_CHROME_EXTENSION_BANNER: false
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

      this.api = new window.JitsiMeetExternalAPI(this.jitsiDomain, options);
      this.currentRoom = config.roomName;
      
      // Set up basic event handlers
      this.setupBasicEventHandlers();
      
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

  // Setup basic event handlers
  private setupBasicEventHandlers(): void {
    if (!this.api) return;

    this.api.addEventListener('readyToClose', () => {
      console.log('Jitsi conference ready to close');
      this.currentRoom = null;
    });

    this.api.addEventListener('participantRoleChanged', (event: any) => {
      console.log('Participant role changed:', event);
    });

    this.api.addEventListener('passwordRequired', () => {
      console.log('Password required for room');
    });
  }

  // Room management methods
  getCurrentRoom(): string | null {
    return this.currentRoom;
  }

  isConferenceActive(): boolean {
    return this.api !== null && this.currentRoom !== null;
  }

  // Security methods
  setPassword(password: string): void {
    if (this.api) {
      this.api.executeCommand('password', password);
    }
  }

  lockRoom(): void {
    if (this.api) {
      this.api.executeCommand('lockRoom', true);
    }
  }

  unlockRoom(): void {
    if (this.api) {
      this.api.executeCommand('lockRoom', false);
    }
  }

  // Moderator controls
  muteParticipant(participantId: string): void {
    if (this.api) {
      this.api.executeCommand('muteParticipant', participantId);
    }
  }

  muteEveryone(): void {
    if (this.api) {
      this.api.executeCommand('muteEveryone');
    }
  }

  kickParticipant(participantId: string): void {
    if (this.api) {
      this.api.executeCommand('kickParticipant', participantId);
    }
  }

  // Waiting room controls
  admitParticipant(participantId: string): void {
    if (this.api) {
      this.api.executeCommand('grantModerator', participantId);
    }
  }

  // Recording controls
  startRecording(): void {
    if (this.api) {
      this.api.executeCommand('startRecording', {
        mode: 'file'
      });
    }
  }

  stopRecording(): void {
    if (this.api) {
      this.api.executeCommand('stopRecording', 'file');
    }
  }

  // Cleanup
  dispose(): void {
    if (this.api) {
      this.api.dispose();
      this.api = null;
      this.currentRoom = null;
    }
  }

  // Generate secure room names
  static generateRoomName(circleId: string, sessionId?: string): string {
    const timestamp = Date.now();
    const randomSuffix = Math.random().toString(36).substring(2, 8);
    const base = `ic-${circleId}-${randomSuffix}`;
    return sessionId ? `${base}-${sessionId.substring(0, 8)}` : `${base}-${timestamp.toString().substring(-6)}`;
  }

  // Generate room password
  static generateRoomPassword(): string {
    return Math.random().toString(36).substring(2, 10).toUpperCase();
  }

  // Validate room name format
  static isValidRoomName(roomName: string): boolean {
    return /^ic-[a-zA-Z0-9\-_]+$/.test(roomName);
  }
}

const jitsiService = new JitsiService();

export default jitsiService;
export { JitsiService };
export type { JitsiMeetConfig };
/**
 * Thalos Prime Agent Session Module (Node.js)
 * 
 * Deterministic agent session management with explicit control
 */

const { v4: uuidv4 } = require('uuid');

/**
 * Session states
 */
const SessionState = {
  INITIALIZED: 'initialized',
  RUNNING: 'running',
  PAUSED: 'paused',
  RESUMING: 'resuming',
  TERMINATED: 'terminated',
  ERROR: 'error'
};

/**
 * Agent Session class
 */
class AgentSession {
  constructor(options = {}) {
    this.sessionId = options.sessionId || uuidv4();
    this.state = options.state || SessionState.INITIALIZED;
    this.createdAt = options.createdAt || new Date();
    this.updatedAt = options.updatedAt || new Date();
    this.metadata = options.metadata || {};
    this.errorMessage = options.errorMessage || null;
    this.stateHistory = options.stateHistory || [];
    this.transitionCount = options.transitionCount || 0;
  }

  /**
   * Start the session
   */
  start() {
    if (![SessionState.INITIALIZED, SessionState.PAUSED].includes(this.state)) {
      throw new Error(
        `Cannot start session from state ${this.state}. Must be INITIALIZED or PAUSED.`
      );
    }
    return this._transitionTo(SessionState.RUNNING);
  }

  /**
   * Pause the session
   */
  pause() {
    if (this.state !== SessionState.RUNNING) {
      throw new Error(
        `Cannot pause session from state ${this.state}. Must be RUNNING.`
      );
    }
    return this._transitionTo(SessionState.PAUSED);
  }

  /**
   * Resume the session
   */
  resume() {
    if (this.state !== SessionState.PAUSED) {
      throw new Error(
        `Cannot resume session from state ${this.state}. Must be PAUSED.`
      );
    }
    return this._transitionTo(SessionState.RUNNING);
  }

  /**
   * Terminate the session
   */
  terminate() {
    if (this.state === SessionState.TERMINATED) {
      throw new Error('Session is already terminated.');
    }
    return this._transitionTo(SessionState.TERMINATED);
  }

  /**
   * Mark session as errored
   */
  markError(errorMessage) {
    const newSession = this._transitionTo(SessionState.ERROR);
    newSession.errorMessage = errorMessage;
    return newSession;
  }

  /**
   * Internal transition method
   */
  _transitionTo(newState) {
    const historyEntry = {
      from: this.state,
      to: newState,
      timestamp: new Date().toISOString()
    };

    return new AgentSession({
      sessionId: this.sessionId,
      state: newState,
      createdAt: this.createdAt,
      updatedAt: new Date(),
      metadata: { ...this.metadata },
      errorMessage: this.errorMessage,
      stateHistory: [...this.stateHistory, historyEntry],
      transitionCount: this.transitionCount + 1
    });
  }

  /**
   * Convert to plain object
   */
  toObject() {
    return {
      sessionId: this.sessionId,
      state: this.state,
      createdAt: this.createdAt.toISOString(),
      updatedAt: this.updatedAt.toISOString(),
      metadata: this.metadata,
      errorMessage: this.errorMessage,
      stateHistory: this.stateHistory,
      transitionCount: this.transitionCount
    };
  }

  /**
   * Create from plain object
   */
  static fromObject(data) {
    return new AgentSession({
      sessionId: data.sessionId,
      state: data.state,
      createdAt: new Date(data.createdAt),
      updatedAt: new Date(data.updatedAt),
      metadata: data.metadata || {},
      errorMessage: data.errorMessage,
      stateHistory: data.stateHistory || [],
      transitionCount: data.transitionCount || 0
    });
  }
}

module.exports = {
  AgentSession,
  SessionState
};

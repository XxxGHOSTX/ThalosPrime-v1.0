/**
 * Session Manager (Node.js)
 * 
 * Manages multiple agent sessions
 */

const { AgentSession, SessionState } = require('./session');

class SessionManager {
  constructor() {
    this.sessions = new Map();
    this.operationLog = [];
  }

  /**
   * Create a new session
   */
  createSession(metadata = {}) {
    const session = new AgentSession({ metadata });
    this.sessions.set(session.sessionId, session);
    this._logOperation('create', session.sessionId);
    return session;
  }

  /**
   * Get a session by ID
   */
  getSession(sessionId) {
    return this.sessions.get(sessionId);
  }

  /**
   * Start a session
   */
  startSession(sessionId) {
    const session = this._getSessionOrThrow(sessionId);
    const updatedSession = session.start();
    this.sessions.set(sessionId, updatedSession);
    this._logOperation('start', sessionId);
    return updatedSession;
  }

  /**
   * Pause a session
   */
  pauseSession(sessionId) {
    const session = this._getSessionOrThrow(sessionId);
    const updatedSession = session.pause();
    this.sessions.set(sessionId, updatedSession);
    this._logOperation('pause', sessionId);
    return updatedSession;
  }

  /**
   * Resume a session
   */
  resumeSession(sessionId) {
    const session = this._getSessionOrThrow(sessionId);
    const updatedSession = session.resume();
    this.sessions.set(sessionId, updatedSession);
    this._logOperation('resume', sessionId);
    return updatedSession;
  }

  /**
   * Terminate a session
   */
  terminateSession(sessionId) {
    const session = this._getSessionOrThrow(sessionId);
    const updatedSession = session.terminate();
    this.sessions.set(sessionId, updatedSession);
    this._logOperation('terminate', sessionId);
    return updatedSession;
  }

  /**
   * List sessions, optionally filtered by state
   */
  listSessions(state = null) {
    const sessions = Array.from(this.sessions.values());
    if (state) {
      return sessions.filter(s => s.state === state);
    }
    return sessions;
  }

  /**
   * Get session count
   */
  getSessionCount(state = null) {
    return this.listSessions(state).length;
  }

  /**
   * Cleanup terminated sessions
   */
  cleanupTerminatedSessions() {
    const terminatedIds = [];
    for (const [sessionId, session] of this.sessions.entries()) {
      if (session.state === SessionState.TERMINATED) {
        terminatedIds.push(sessionId);
      }
    }

    for (const sessionId of terminatedIds) {
      this.sessions.delete(sessionId);
    }

    this._logOperation('cleanup', `${terminatedIds.length} sessions`);
    return terminatedIds.length;
  }

  /**
   * Get operation log
   */
  getOperationLog() {
    return [...this.operationLog];
  }

  /**
   * Internal helper to get session or throw
   */
  _getSessionOrThrow(sessionId) {
    const session = this.sessions.get(sessionId);
    if (!session) {
      throw new Error(`Session ${sessionId} not found`);
    }
    return session;
  }

  /**
   * Internal helper to log operations
   */
  _logOperation(operation, target) {
    this.operationLog.push({
      operation,
      target,
      timestamp: new Date().toISOString()
    });
  }
}

module.exports = SessionManager;

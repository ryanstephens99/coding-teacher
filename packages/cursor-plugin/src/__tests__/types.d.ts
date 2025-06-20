/**
 * Type declarations for test environment
 */

declare global {
  namespace NodeJS {
    interface Global {
      mockVSCode: any;
    }
  }

  var mockVSCode: any;
}

export {}; 
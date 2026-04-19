/**
 * V31 Marius TPL - Test Suite
 */

class V31TestSuite {
    constructor() {
        this.tests = [];
        this.results = [];
    }
    
    addTest(name, fn) {
        this.tests.push({ name, fn });
    }
    
    async runAll() {
        console.log('Running V31 Test Suite...');
        this.results = [];
        
        for (const test of this.tests) {
            try {
                await test.fn();
                this.results.push({ name: test.name, status: 'PASS' });
                console.log(`✅ ${test.name}`);
            } catch (error) {
                this.results.push({ name: test.name, status: 'FAIL', error: error.message });
                console.log(`❌ ${test.name}: ${error.message}`);
            }
        }
        
        return this.results;
    }
    
    static createDefaultTests() {
        const suite = new V31TestSuite();
        
        suite.addTest('Dashboard Initialization', () => {
            if (!window.v31Dashboard) throw new Error('Dashboard not initialized');
        });
        
        suite.addTest('Symbol Grid Loaded', () => {
            if (!window.v31Dashboard.symbols || window.v31Dashboard.symbols.length === 0) {
                throw new Error('No symbols loaded');
            }
        });
        
        suite.addTest('WebSocket Connection Available', () => {
            if (typeof WebSocket === 'undefined') {
                throw new Error('WebSocket not supported');
            }
        });
        
        return suite;
    }
}

// Export for use
if (typeof module !== 'undefined') {
    module.exports = V31TestSuite;
}

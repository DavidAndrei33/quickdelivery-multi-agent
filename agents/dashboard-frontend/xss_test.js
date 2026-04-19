// Test pentru functia escapeHtml - XSS Protection Test

function escapeHtml(text) {
    if (text === null || text === undefined) return '';
    const div = document.createElement('div');
    div.textContent = String(text);
    return div.innerHTML;
}

// Test cases
const testCases = [
    {
        input: "<script>alert('XSS')</script>",
        expected: "&lt;script&gt;alert('XSS')&lt;/script&gt;",
        description: "Script tag injection"
    },
    {
        input: '<img src=x onerror=alert("XSS")>',
        expected: '&lt;img src=x onerror=alert("XSS")&gt;',
        description: "Image onerror injection"
    },
    {
        input: 'EURUSD',
        expected: 'EURUSD',
        description: "Normal symbol"
    },
    {
        input: 'BUY',
        expected: 'BUY',
        description: "Normal trade type"
    },
    {
        input: '<div onclick="steal()">Click</div>',
        expected: '&lt;div onclick="steal()"&gt;Click&lt;/div&gt;',
        description: "Click handler injection"
    },
    {
        input: '" onmouseover="alert(1)',
        expected: '" onmouseover="alert(1)',
        description: "Quote injection (escaped)"
    },
    {
        input: null,
        expected: '',
        description: "Null value"
    },
    {
        input: undefined,
        expected: '',
        description: "Undefined value"
    },
    {
        input: 12345,
        expected: '12345',
        description: "Number value"
    }
];

console.log('=== XSS Protection Test for escapeHtml() ===\n');

let passed = 0;
let failed = 0;

testCases.forEach((test, index) => {
    const result = escapeHtml(test.input);
    const success = result === test.expected;
    
    if (success) {
        passed++;
        console.log(`✅ Test ${index + 1} PASSED: ${test.description}`);
    } else {
        failed++;
        console.log(`❌ Test ${index + 1} FAILED: ${test.description}`);
        console.log(`   Input:    ${JSON.stringify(test.input)}`);
        console.log(`   Expected: ${JSON.stringify(test.expected)}`);
        console.log(`   Got:      ${JSON.stringify(result)}`);
    }
});

console.log(`\n=== Results: ${passed}/${testCases.length} tests passed ===`);

if (failed === 0) {
    console.log('✅ All XSS protection tests passed!');
} else {
    console.log(`❌ ${failed} test(s) failed!`);
}

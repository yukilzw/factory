process.stdout.write(process.cwd());
process.argv.forEach(function(val, index, array) {
    process.stdout.write('\r\n' + index + ' : ' + val);
});
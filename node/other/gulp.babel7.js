var gulp = require('gulp');
var gulpBabel = require('gulp-babel');

gulp.src('./es6.js')
    .pipe(gulpBabel({
        'presets': [
            '@babel/preset-env',
            '@babel/preset-react'
        ],
        'plugins': [
            ['@babel/plugin-proposal-decorators', { 'legacy': true }],
            '@babel/proposal-class-properties',
            ['@babel/plugin-transform-runtime', { 'corejs': 2 }]
        ]
    })).on('error', (err) => console.log(err))
    .pipe(gulp.dest('./babel'));
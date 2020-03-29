const mix = require("laravel-mix");

mix.sass('assets/sass/main.scss', 'static/css')
    .options({
        postCss: [
            require('postcss-css-variables')()
        ]
    })
    .sourceMaps();
mix.js('assets/js/app.js', 'static/js/index.js')
    .sourceMaps();

mix.disableNotifications();
const mix = require("laravel-mix");
mix.setPublicPath('./');
mix.sass('assets/sass/main.scss', 'static/css')
    .options({
        postCss: [
            require('postcss-css-variables')()
        ]
    })
    .sourceMaps();
mix.js('assets/js/index.js', 'static/js/index.js')
    .sourceMaps();
mix.version();

mix.disableNotifications();
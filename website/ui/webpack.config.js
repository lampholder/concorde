const Path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

function create_config(options) {
    return {
        entry: './src/index.js',
        output: {
            path: Path.resolve(__dirname, 'dist'),
            filename: './bin/app.js'
        },
        module: {
            loaders: [
                {
                    test: /\.css$/,
                    loader: 'style-loader!css-loader'
                },
                {
                    test: /\.(jpg|png|svg)$/,
                    loader: 'file-loader'
                },
                {
                    test: /config\.js$/,
                    loader: 'string-replace-loader',
                    query: {
                        multiple: [
                            { search: 'REGISTRATION_API_URL', replace: options.registrationApiUrl },
                            { search: 'SLACK_TEAM', replace: options.slackTeam },
                            { search: 'MATRIX_DOMAIN', replace: options.matrixDomain },
                            { search: 'RIOT_URL', replace: options.riotUrl }
                        ]
                    }
                }
            ]
        },
        resolve: {
            alias: {
                Resources: Path.resolve(__dirname, 'resources')
            }
        },
        plugins: [
            new HtmlWebpackPlugin({
                title: 'Slack -> Riot.im Migration Manager'
            })
        ]
    };
}

module.exports = function(env) {
    return create_config(env);
};

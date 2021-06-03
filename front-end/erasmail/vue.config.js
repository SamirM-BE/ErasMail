module.exports = {
    devServer: {
        proxy: {
            '^/api/': {
                target: 'http://web:8000',
            }
        }
    },
}
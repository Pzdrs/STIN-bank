function clearPaginationUrl(query_parameter) {
    let url = window.location.href.split('?')[0]; // Get the base URL
    let queryParameters = new URLSearchParams(window.location.search);
    queryParameters.delete(query_parameter);
    if (queryParameters.toString()) {
        url += '?' + queryParameters.toString(); // Add the remaining query parameters
    }
    if (window.location.hash) {
        url += window.location.hash; // Add the fragment identifier if present
    }
    window.location.replace(url);
}
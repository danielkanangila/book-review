import $ from 'jquery';

class Router {
    constructor() {
        this.routes = [];
        this.request = window.location;
    }

    /**
     *
     * @param route
     */
    route(route) {
        this.routes.push(route)
    }

    run() {
        this.routes.forEach(route => {
            // verify if current location pathname match with any of element if routes array
            // if yes call the corresponding component and pass the props.
            // if not and route have component prop call it.
            if (this.request.pathname === route.path) {
                // Retrieve props from each route
                const props = route.props || {};
                // set jquery and window
                props.$ = $;
                props.$window = $(window);
                props.$document = $(document);
                // set location window to component props
                props.location = this.request;
                // check if element prop exist in route object
                // select the corresponding element in the DOM
                // and set this new DOM element to $this prop object to props object,
                // else set props element to empty.
                if (route.element) {
                    props.$this = $(route.element);
                } else {
                    props.$this = {};
                }

                // if component return a html, append this html to the element.
                const result = route.component({...props});

                if (result && $(route.element)) {
                    $(route.element).append(result);
                }
            } else {
                if (route.component && !route.path) {
                    route.component()
                }
            }
        })
    }
}

export default new Router();
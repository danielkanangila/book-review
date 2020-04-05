import $ from 'jquery';

class Router {
    constructor() {
        this.routes = [];
        this.request = window.location;
        this.mathcedRoute = {};
    }

    /**
     *
     * @param route
     */
    route(route) {
        this.routes.push(route)
    }

    run() {
        this._loadInitialRoute();
        const props = this.mathcedRoute.props || {};
        props.$ = $;
        props.$window = $(window);
        props.$document = $(document);
        props.location = this.request;
        props.params = this.mathcedRoute.params;

        // check if element prop exist in route object
        // select the corresponding element in the DOM
        // and set this new DOM element to $this prop object to props object,
        // else set props element to empty.

        if (this.mathcedRoute.element) {
            props.$this = document.querySelector(this.mathcedRoute.element);
        } else {
            props.$this = {}
        }
        const instance = this.mathcedRoute.component;
        // if component return a html, append this html to the element.
        const result = instance.call(this, {...props});

        /*
        this.routes.forEach(route => {
            // verify if current location pathname match with any of element if routes array
            // if yes call the corresponding component and pass the props.
            // if not and route have component prop call it.
            //console.log(decodeURIComponent(this.request.pathname));
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
                    props.$this = document.querySelector(route.element);
                } else {
                    props.$this = {};
                }

                // if component return a html, append this html to the element.
                const result = route.component.call(this, {...props});

                if (result && $(route.element)) {
                    $(route.element).append(result);
                }
            } else {
                if (route.component && !route.path) {
                    route.component()
                }
            }
        })

         */
    }

    _matchUrlToRoute(urlSegments) {
        const routeParams = {};
        const matchedRoute = this.routes.find(route => {
            const routePathSegments = route.path.split('/').slice(1);

            if (routePathSegments.length !== urlSegments.length) {
                return false;
            }

            const match = routePathSegments.every((routePathSegment, i) => {
                return routePathSegment === urlSegments[i] || routePathSegment[0] === ':';
            });

            if (match) {
                routePathSegments.forEach((segment, i) => {
                    if (segment[0] === ':') {
                        const propName = segment.slice(1);
                        routeParams[propName] = decodeURIComponent(urlSegments[i]);
                    }
                })
            }

            return match
        });

        this.mathcedRoute = {...matchedRoute, params: routeParams};
    }

    _loadInitialRoute() {
        const pathnameSplit = this.request.pathname.split('/');
        const pathSegments = pathnameSplit.length > 1 ? pathnameSplit.slice(1) : ''
        this._matchUrlToRoute(pathSegments);
    }
}

export default new Router();
jQuery(document).ready(function (e) {
    e("body").not(".a-agent-iphone") && /iPhone/i.test(navigator.userAgent || navigator.vendor || window.opera) && e("body").addClass("a-agent-iphone"), e("body").not(".a-agent-ipad") && /iPad/i.test(navigator.userAgent || navigator.vendor || window.opera) && e("body").addClass("a-agent-ipad"), e("body").not(".a-agent-touch") && ("ontouchstart" in window || navigator.msMaxTouchPoints) && e("body").addClass("a-agent-touch"), (-1 !== navigator.userAgent.indexOf("MSIE") || navigator.appVersion.indexOf("Trident/") > 0) && e("body").addClass("a-agent-explorer"), window.navigator.userAgent.indexOf("Edge") > -1 && e("body").addClass("a-agent-edge"), e("body.a-agent-explorer, body.a-agent-edge").find(".card-horizontal .card-img").each(function () {
        var o = e(this),
            n = o.attr("src");
        o.parent(".card-img-container").css("background-image", "url(" + n + ")"), o.parent(".carousel-item").css("background-image", "url(" + n + ")")
    }), e(".a-icon-set-expandable a").on("click", function (o) {
        e(this).hasClass("a-icon-set-item-action") || (o.preventDefault(), o.stopPropagation()), e(this).parent(".a-icon-set-expandable").toggleClass("open")
    }), e(".carousel").each(function () {
        var o = e(this),
            n = o.data("height");
        o.css("min-height", n)
    }), window.paceOptions = {
        startOnPageLoad: !0,
        restartOnRequestAfter: !1
    }, Pace.on("done", function () {
        setTimeout(function () {
            ! function (o) {
                o.each(function () {
                    var o = e(this),
                        n = o.attr("data-os-animation"),
                        a = o.attr("data-os-animation-delay");
                    o.css({
                        "-webkit-animation-delay": a,
                        "-moz-animation-delay": a,
                        "animation-delay": a
                    }), new Waypoint({
                        element: o[0],
                        handler: function () {
                            e(this.element).addClass("animated").addClass(n)
                        },
                        offset: "90%"
                    })
                })
            }(e(".a-os-animation"))
        }, 500)
    })
});
var map = window.map || {
    map_type: "ROADMAP",
    auto_zoom: "manual",
    map_zoom: 7,
    map_scrollable: "on",
    map_style: "",
    addresses: ["London", "Paris"],
    latlngs: ["51.511084, -0.133202", "51.506623, -0.111916"],
    labels: ["London", "Paris"],
    auto_center: "auto",
    center_latlng: "",
    show_markers: "on",
    markerURL: "assets/images/marker.png"
};
jQuery(document).ready(function (e) {
    function o(o, a) {
        void 0 === window.google ? e.getScript("https://maps.googleapis.com/maps/api/js?v=3.29", function () {
            n(o, a)
        }) : n(o, a)
    }

    function n(o, n) {
        var t = function (e, o) {
            var n = {
                zoom: parseInt(o.map_zoom, 10),
                scrollwheel: !1,
                draggable: "on" === o.map_scrollable,
                mapTypeId: google.maps.MapTypeId[o.map_type]
            };
            "blackwhite" === o.map_style && (n.styles = [{
                stylers: [{
                    saturation: -100
                }]
            }]);
            "retro" === o.map_style && (n.styles = [{
                featureType: "administrative",
                elementType: "labels.text.fill",
                stylers: [{
                    color: "#575e66"
                }]
            }, {
                featureType: "landscape",
                elementType: "all",
                stylers: [{
                    color: "#f8f2e6"
                }]
            }, {
                featureType: "poi",
                elementType: "all",
                stylers: [{
                    visibility: "off"
                }]
            }, {
                featureType: "road",
                elementType: "all",
                stylers: [{
                    saturation: -100
                }, {
                    lightness: 45
                }, {
                    visibility: "simplified"
                }]
            }, {
                featureType: "road.highway",
                elementType: "all",
                stylers: [{
                    visibility: "simplified"
                }]
            }, {
                featureType: "road.highway",
                elementType: "labels",
                stylers: [{
                    visibility: "off"
                }]
            }, {
                featureType: "road.arterial",
                elementType: "labels.icon",
                stylers: [{
                    visibility: "off"
                }]
            }, {
                featureType: "transit",
                elementType: "all",
                stylers: [{
                    visibility: "off"
                }]
            }, {
                featureType: "water",
                elementType: "all",
                stylers: [{
                    color: "#c9bfac"
                }, {
                    visibility: "on"
                }, {
                    saturation: "0"
                }, {
                    lightness: "50"
                }]
            }]);
            return new google.maps.Map(e[0], n)
        }(o, n);
        n.bounds = new google.maps.LatLngBounds,
            function (o, n, t) {
                t.markers = [], t.addresses ? function (o, n) {
                    var t = 0;
                    e.each(n.addresses, function (e, s) {
                        (new google.maps.Geocoder).geocode({
                            address: s
                        }, function (s, i) {
                            if (i === google.maps.GeocoderStatus.OK) {
                                if (void 0 !== s[0]) {
                                    var r = s[0].geometry.location;
                                    n.markers[e] = {
                                        position: new google.maps.LatLng(r.lat(), r.lng())
                                    }, n.bounds.extend(n.markers[e].position)
                                }++t === n.addresses.length && a(o, n)
                            }
                        })
                    })
                }(o, t) : t.latlngs && function (e, o) {
                    for (var n = 0; n < o.latlngs.length; n++) {
                        var t = o.latlngs[n].split(",");
                        o.markers[n] = {
                            position: new google.maps.LatLng(t[0], t[1])
                        }, o.bounds.extend(o.markers[n].position)
                    }
                    a(e, o)
                }(o, t)
            }(t, 0, n);
        var s;
        "manual" === n.auto_zoom ? s = google.maps.event.addListener(t, "bounds_changed", function () {
            this.setZoom(parseInt(n.map_zoom)), google.maps.event.removeListener(s)
        }) : void 0 !== s && google.maps.event.removeListener(s)
    }

    function a(o, n) {
        e.each(n.markers, function (e, a) {
                var t = {
                        position: a.position,
                        icon: n.markerURL,
                        visible: "on" === n.show_markers,
                        map: o
                    },
                    s = new google.maps.Marker(t);
                if (s.setMap(o), void 0 !== n.labels[e]) {
                    var i = new google.maps.InfoWindow({
                        content: n.labels[e]
                    });
                    google.maps.event.addListener(s, "click", function () {
                        i.open(o, this)
                    })
                }
            }),
            function (e, o) {
                if ("auto" === o.auto_center) "manual" === o.auto_zoom ? e.setCenter(o.bounds.getCenter()) : e.fitBounds(o.bounds);
                else if ("" !== o.center_latlng) {
                    var n = o.center_latlng.split(","),
                        a = new google.maps.LatLng(n[0], n[1]);
                    e.setCenter(a)
                } else e.fitBounds(o.bounds)
            }(o, n)
    }
    e(".google-map").each(function () {
        var n = e(this),
            a = window[n.attr("id")];
        e(window).resize(function () {
            o(n, a)
        }), o(n, a)
    })
}), jQuery(document).ready(function (e) {
    function o(o) {
        e(".a-nav-menu .a-nav-list").slideToggle(), e(".a-nav-menu .a-nav-widget").slideToggle(), e("#nav-toggle").toggleClass("active"), o.preventDefault()
    }!e("body").hasClass("a-agent-touch") && e(".a-nav").hasClass("a-nav-hover") ? e(".a-nav-menu ul li").on("mouseover", function () {
        e(this).find(".a-nav-dropdown").removeClass("closed")
    }).on("mouseout", function () {
        e(this).find(".a-nav-dropdown").addClass("closed")
    }) : e(".a-nav-menu ul li a:not(:only-child)").on("click", function (o) {
        e(this).siblings(".a-nav-dropdown").toggleClass("closed"), e(".a-nav-dropdown").not(e(this).siblings()).addClass("closed"), o.stopPropagation(), o.preventDefault()
    }), e("html").on("click", function () {
        e(".a-nav-dropdown").addClass("closed")
    }), e("#content").on("click", function (n) {
        e("#nav-toggle").hasClass("active") && o(n)
    }), e("body").on("click", "#nav-toggle", function (e) {
        o(e)
    });
    var n = e("body").find(".a-header:not(.a-header-side) .a-nav-sticky");
    n.length > 0 && (new Waypoint.Sticky({
        element: n[0],
        stuckClass: "a-nav-stuck"
    }), new Waypoint({
        element: document.body,
        offset: -200,
        handler: function (e) {
            "down" === e ? n.addClass("a-nav-scrolled") : n.removeClass("a-nav-scrolled")
        }
    })), new Waypoint({
        element: document.body,
        offset: -200,
        handler: function (o) {
            "down" === o ? e(".a-go-top").removeClass("hide") : e(".a-go-top").addClass("hide")
        }
    }), e("body").on("click", ".a-go-top", function (o) {
        o.preventDefault(), e("html, body").animate({
            scrollTop: 0
        }, 300)
    })
}), jQuery(document).ready(function (e) {
    function o() {
        n.removeClass("a-content-box-moved"), s.removeClass("a-search-widget-container-open"), i.blur(), i.value = ""
    }
    var n = e(".a-content-box"),
        a = e(".a-search-widget-button-open"),
        t = e(".a-search-widget-button-close"),
        s = e(".a-search-widget-container"),
        i = e(".a-search-widget-input");
    a.on("click", function (e) {
        n.addClass("a-content-box-moved"), s.addClass("a-search-widget-container-open"), setTimeout(function () {
            i.focus()
        }, 600), e.preventDefault()
    }), t.on("click", o), e(document).on("keyup", function (e) {
        27 === e.keyCode && (console.log("close"), o())
    })
});
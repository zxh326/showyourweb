!
function() {
    function o(w, v, i) {
        return w.getAttribute(v) || i
    }
    function j(i) {
        return document.getElementsByTagName(i)
    }
    function l() {
        var i = j("script"),
        w = i.length,
        v = i[w - 1];
        return {
            l: w,
            z: o(v, "zIndex", -1),
            o: o(v, "opacity", 0.5),
            c: o(v, "color", "0,0,0"),
            n: o(v, "count", 99)
        }
    }
    function k() {
        r = u.width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth,
        n = u.height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight
    }
    function b() {
        e.clearRect(0, 0, r, n);
        var w = [f].concat(t);
        var x, v, A, B, z, y;
        t.forEach(function(i) {
            i.x += i.xa,
            i.y += i.ya,
            i.xa *= i.x > r || i.x < 0 ? -1 : 1,
            i.ya *= i.y > n || i.y < 0 ? -1 : 1,
            e.fillRect(i.x - 0.5, i.y - 0.5, 1, 1);
            // var rgb_r = Math.ceil(Math.random()*255);
            // var rgb_g = Math.ceil(Math.random()*255);
            // var rgb_b = Math.ceil(Math.random()*255);
            // s.c = o(s.v,"color","" + rgb_r +"," + rgb_g + "," + rgb_b + "");
            var hours = new Date().getHours();
            var Minutes = new Date().getMinutes();
            var Seconds = new Date().getSeconds();

            if (hours < 10) {
                hours = '0' + hours;
            }
            if (Seconds < 10) {
                Seconds = '0' + Seconds;
            }
            if (Minutes < 10) {
                Minutes = '0' + Minutes;
            }

            var str = '#' + hours + Minutes + Seconds;
            // console.log(str)
            // $("#title").attr("style","color:"+ s);
            // $("#ftitle").attr("style","color:"+ s);
            // $("#time").html(s);
            // var str = s.colorRgb();
            for (v = 0; v < w.length; v++) {
                x = w[v];
                if (i !== x && null !== x.x && null !== x.y) {
                    B = i.x - x.x,
                    z = i.y - x.y,
                    y = B * B + z * z;
                    y < x.max && (x === f && y >= x.max / 2 && (i.x -= 0.03 * B, i.y -= 0.03 * z), A = (x.max - y) / x.max, e.beginPath(), e.lineWidth = A / 2, e.strokeStyle = str, e.moveTo(i.x, i.y), e.lineTo(x.x, x.y), e.stroke())
                }
            }
            w.splice(w.indexOf(i), 1)
        }),
        m(b)
    }
    var u = document.createElement("canvas"),
    s = l(),
    c = "c_n" + s.l,
    e = u.getContext("2d"),
    r,
    n,
    m = window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame ||
    function(i) {
        window.setTimeout(i, 1000 / 45)
    },
    a = Math.random,
    f = {
        x: null,
        y: null,
        max: 20000
    };
    u.id = c;
    u.style.cssText = "position:fixed;top:0;left:0;z-index:" + s.z + ";opacity:" + s.o;
    j("body")[0].appendChild(u);
    k(),
    window.onresize = k;
    window.onmousemove = function(i) {
        i = i || window.event,
        f.x = i.clientX,
        f.y = i.clientY
    },
    window.onmouseout = function() {
        f.x = null,
        f.y = null
    };
    for (var t = [], p = 0; s.n > p; p++) {
        var h = a() * r,
        g = a() * n,
        q = 2 * a() - 1,
        d = 2 * a() - 1;
        t.push({
            x: h,
            y: g,
            xa: q,
            ya: d,
            max: 6000
        })
    }
    setTimeout(function() {
        b()
    },
    100)
} ();

String.prototype.colorRgb = function(){
    var reg = /^#([0-9a-fA-f]{3}|[0-9a-fA-f]{6})$/; 
    var sColor = this.toLowerCase();  
    if(sColor && reg.test(sColor)){  
        if(sColor.length === 4){  
            var sColorNew = "#";  
            for(var i=1; i<4; i+=1){  
                sColorNew += sColor.slice(i,i+1).concat(sColor.slice(i,i+1));     
            }  
            sColor = sColorNew;  
        }  
        //处理六位的颜色值  
        var sColorChange = [];  
        for(var i=1; i<7; i+=2){  
            sColorChange.push(parseInt("0x"+sColor.slice(i,i+2)));    
        }  
        return "rgba(" + sColorChange.join(",") + ")";  
    }
    else{  
        return sColor;    
    }
};
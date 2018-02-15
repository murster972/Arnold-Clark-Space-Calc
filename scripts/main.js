window.addEventListener("resize", placeStars, false);
window.addEventListener("load", placeStars, false);

//Info for intros found at each Planets Wikipedia page
planet_intro = {"mercury": "The smallest and innermost planet to the sun Mercury has the shortest orbital period in the\
                             Solar System, at just 88 days. It's named after the messsenger to the gods, Roman diety Mercury.",
                 "venus": "The second planet from the sun Venus has an orbital period of 224 days. It is the\
                           second-brightness natrual object in the sky, bright enought to cast shadows at night. Named\
                           after the Roman goddess of love and beauty.",
                 "earth": "Earth is rather unique, being the only known object in the Universe known to harbour life.\
                           Formed over 4 billion years ago, Earth is the third planet from the sun and has an orbital\
                           period of 365 days. The origin of Earths name is unknown, and is the only planet not named\
                           after a Greek or Roman god/goddess.",
                 "mars": "Mars is the fourth planet from the sun and the second smallest in the Solar System. It has\
                          an orbital period of 1.89 years. Named after the Roman god of war, Mars is also referred to\
                          as the \"Red Planet\". There are ongoing investigations assessing Mars' ability to harbour life.",
                 "jupiter": "Jupiter is the largest planet in the Solar System and fifth from the sun. With an orbital period\
                             of 11.86 years. Being mostly compossed of gasses, Jupiter is known as a gas giant. Named\
                             after the Roman god Jupiter. The third-brightest object in the night sky, after the Moon and Venus.",
                 "saturn": "The sixth planet from the Sun, Saturn is the second largest planet in the Solar System and has the most\
                            extensive planetary ring system of any planet in the Solar System. Saturn is known as a gas giant, as it's\
                            compossed mostly of gasses. With an orbital period of 29.46 years and Saturn is named after the Roman god\
                            of agriculture.",
                 "uranus": "Uranus is the seventh planet from the Sun. A gas giant Uranus is compossed of elements heavier than hydrogen and helium,\
                            and is referred to as an ice giant (along with Neptune), to distinguish it from the larger gas planets Jupiter ans Saturn. Uranus' name is\
                            derived from the Greek god of the sky Ouranos, and is the only planet whose name's derived from greek mythology.",
                 "neptune": "The eighth planet from the sun, Neptune is the farthest known planet in the Solar System. A gas giant, Neptune\
                             is compossed mostly of gasses, but is compossed of heaver elements than Saturn and Jupiter and is classified as an\
                             ice giant (along with Uranus). It has an orbital period of 164.8 years and is named after the Roman god of the sea",
                 "pluto": "Discovered in 1930, Pluto was originally considered to be the ninth planet in the Solar System, but was reclassified\
                           as a dwarf planet in August 2006. It has an orbital period of 248 years, longer than any of the known planets in the\
                           Solar System. Named after the Roman god of the underworld, Pluto was named by an 11-year-old girl."}

planets = ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"];

earth_years = {"mercury": 0.2408467, "venus": 0.61519726, "earth": 1, "mars": 1.8808158, "jupiter": 11.862615, "saturn": 29.447498, "uranus": 84.016846, "neptune": 164.79132, "pluto": 248}

$(document).ready(function(){
    placeStars();

    $(".age_input").val("");

    $(".age_input").on("blur", function(){validateAgeInput(this.id)})

    //display planet info if input valid
    $(".planet").on("click touch", function(){
        if(getInputErrors()){
            $("#info_container").addClass("error_animation");

            setTimeout(function(){$("#info_container").removeClass("error_animation")}, 1100);
        }

        else{
            var id = this.id;
                name = id.substr(0, 1).toUpperCase() + id.substr(1);
                age = calc_space_age();
                p_age = (age * earth_years[id]).toFixed(4);

            $("#planet_info_container").addClass(id).removeClass("hidden");
            $("#planet_title").html(name);
            $("#planet_intro").html(planet_intro[id]);
            $("#earth_age").html(age.toFixed(4) + " years");
            if(id != "earth"){
                $("#planet_name").html("Age on " + name + ": ");
                $("#planet_age").html(p_age + " years");
            }
            else{
                $("#planet_name").html("");
                $("#planet_age").html("");
            }
        }
    })


    //planet page return
    $("#planet_return_arrow").on("click touch", function(){
        $("#planet_info_container").attr("class", "hidden");
    })

    //custom spinners for inputs
    $(".custom_spinner").on("click touch", function(){
        var id = this.className.split(" ")[1];
            input = $("#" + id);
            input_val = input.val();
            input_val = input_val ? parseFloat(input_val) : 0;
            increase = this.id =="increase" ? 1 : -1;

        if(input_val <= 0 && this.id == "decrease") increase = 0;

        input.val(input_val + increase);

        validateAgeInput(id);
    })
})

function getInputErrors(){
    ids = ["years", "months", "days"];
    err = 0;
    for(i = 0; i < ids.length; i++){
        input = $("#" + ids[i]);
        err += input.hasClass("error") ? 1 : 0;
    }

    return err
}

function validateAgeInput(id){
    if(isNaN($("#" + id).val()) || $("#" + id).val() < 0){
        $(".input_wrapper." + id).addClass("error");
        $(".age_symbol." + id).addClass("error");
        $("#" + id).addClass("error");
    }
    else{
        $(".input_wrapper." + id).removeClass("error");
        $(".age_symbol." + id).removeClass("error");
        $("#" + id).removeClass("error");
    }
}

function calc_space_age(){
    var d = parseFloat($("#days").val());
        m = parseFloat($("#months").val());
        y = parseFloat($("#years").val());

    var age = !isNaN(y) ? y : 0;

    age += !isNaN(m) ? m / 12 : 0;
    age += !isNaN(d) ? d / 365 : 0;

    return age;
}

/* generates and places stars on "star_canvas" */
function placeStars(){
    var canvas = document.getElementById("star_canvas");

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    max_x = window.innerWidth;
    max_y = window.innerHeight;

    ctx = canvas.getContext("2d");
    ctx.scale(1.5, 1.5);

    rand = Math.random;

    //varying colours for stars
    star_colours = ["#11104;", "#b6ceff", "#b9c9ff", "#65737e", "#4f5b66", "#343d46", "#3F6DB2", "#F3CCE4", "#0D0F40"];

    //generating and storing all values from 0.2 to 1 with +0.1 increment
    //allows stars to vary in sizes making it more "realistic"
    star_size = [];

    for(i = 0.2; i <= 1.1; i = i += 0.1) star_size.push(i);

    //makes no of stars prop to different screen sizes, e.g. desktop and mobile
    no_stars = (max_x > max_y ? max_x : max_y) * 1;

    for(i = 0; i < no_stars; i++){
        //random pos of star
        x = rand() * max_x;
        y = rand() * max_y;

        //star size - radius of cirlce, and colour of star
        s = star_size[Math.floor(rand() * star_size.length)];
        c = star_colours[Math.floor(rand() * star_colours.length)];

        ctx.fillStyle = c;

        ctx.beginPath();

        ctx.arc(x, y, s, 0, Math.PI * 2);
        ctx.fill();
    }
}

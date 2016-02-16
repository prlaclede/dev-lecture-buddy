$(function (lbLogic, $, undefined) {
    
    lb.init = function () {
        $("#svg-icons").load("/static/pictures/icons.svg");
    }
    
    lb.generateSVG = function (icon, addClass) {
      var image = "<div class='im " + addClass + "'> \
                    <svg viewBox='0 0 25 25'> \
                      <g> \
                        <use xlink:href='#" + icon + "'></use> \
                      </g> \
                    </svg> \
                  </div>";
      return image;
    }
    
    lb.init();
    
}(window.lb = window.lb || {}, jQuery));
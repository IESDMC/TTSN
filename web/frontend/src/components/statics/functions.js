import * as d3 from "d3";
// import epicenterSvg from "@/assets/img/svg/epicenter.svg";
// import stationSvg from "@/assets/img/svg/station.svg?raw";
// import { divIcon, icon } from "leaflet";

export const dataKeys = ["H (km)", "Vp (km/s)", "Vs (km/s)", "Vp/Vs"];

export const getImage = (imgPath) => {
  //   console.debug(img);
  return new URL(`/src/assets/img/${imgPath}`, import.meta.url).href;
};
export const getSvgData = (svgRaw, color, opacity = 0.5) => {
  //in URLs starts a fragment identifier. So, in order to make that work, write %23 instead of #. That is the value of escaped # character.
  color = color.replace("#", "%23");
  // console.debug(svgRaw);
  const svgString = svgRaw
    .replaceAll("${color}", color)
    .replace("${opacity}", opacity);

  return "data:image/svg+xml," + svgString;
};
export const getLeafletIcon = (config) => {
  let iconSvg = config.icon,
    iconSize = config.size,
    color = config.color,
    opacity = config.opacity,
    className = config.className;

  let leafletIcon;
  switch (iconSvg) {
    case "epicenter":
      leafletIcon = L.icon({
        iconUrl: epicenterSvg,
        iconSize: [iconSize, iconSize],
      });
      break;
    default:
      leafletIcon = L.divIcon({
        className: className,
        html: `
          <img     
            src='${getSvgData(stationSvg, color, opacity)}'
            style='
              position: absolute;
              width: ${iconSize * 2}px;
              height: ${iconSize * 2}px;
            '>`,
        iconSize: [iconSize * 2, iconSize * 2],
        iconAnchor: [iconSize, iconSize],
      });
      break;
  }
  // console.debug(leafletIcon);
  return leafletIcon;
};

//==legend
export const LegendColor = {
  // HDomain: [0, 70], //==pga threshold
  // HRange: ["blue", "red"],

  H: d3.schemeRdBu,
};

export const getScale = (key, domain) => {
  let rounding = (number, method = "ceil", place = 1) => {
    let multiplier = Math.pow(10, place);
    return Math[method](number * multiplier) / multiplier;
  };

  const len = 7,
    place = 1;
  let range = domain.reduce((a, b) => b - a);

  let start = rounding(domain[0], "floor", key === dataKeys[0] ? -1 : place),
    interval = key === dataKeys[0] ? 10 : rounding(range / 7, "round");

  // console.debug(key, domain, start, range / 7);
  return d3.scaleThreshold(
    Array.from({ length: len - 1 }, (_, i) =>
      (start + (i + 1) * interval).toFixed(key === dataKeys[0] ? 0 : place)
    ),
    (LegendColor[key] ?? d3.schemeRdBu)[len]
  );
  // return d3.scaleSequentialSqrt([...HDomain], d3.interpolateTurbo);
};

//==@d3/color-legend
export const getColorLegend = ({
  color,
  title,
  tickSize = 6,
  width = 320,
  height = 44 + tickSize,
  marginTop = 18,
  marginRight = 0,
  marginBottom = 16 + tickSize,
  marginLeft = 0,
  ticks = width / 64,
  tickFormat = undefined,
  tickValues = undefined,
  vertical = false,
  reverseColor = false,
} = {}) => {
  function ramp(color, n = 256) {
    const canvas = document.createElement("canvas");
    canvas.width = n;
    canvas.height = 1;
    const context = canvas.getContext("2d");
    for (let i = 0; i < n; ++i) {
      context.fillStyle = color(i / (n - 1));
      context.fillRect(i, 0, 1, 1);
    }
    return canvas;
  }

  const svg = d3
    .create("svg")
    .attr("width", vertical ? height : width)
    .attr("height", vertical ? width : height)
    .attr("viewBox", vertical ? [0, 0, height, width] : [0, 0, width, height])
    .style("overflow", "visible")
    .style("display", "block");

  let tickAdjust = (g) =>
    g.selectAll(".tick line").attr("y1", marginTop + marginBottom - height);
  let x;

  // Continuous
  if (color.interpolate) {
    const n = Math.min(color.domain().length, color.range().length);

    x = color
      .copy()
      .rangeRound(
        d3.quantize(d3.interpolate(marginLeft, width - marginRight), n)
      );

    svg
      .append("image")
      .attr("x", marginLeft)
      .attr("y", marginTop)
      .attr("width", width - marginLeft - marginRight)
      .attr("height", height - marginTop - marginBottom)
      .attr("preserveAspectRatio", "none")
      .attr(
        "xlink:href",
        ramp(
          color.copy().domain(d3.quantize(d3.interpolate(0, 1), n))
        ).toDataURL()
      );
  }

  // Sequential
  else if (color.interpolator) {
    x = Object.assign(
      color
        .copy()
        .interpolator(d3.interpolateRound(marginLeft, width - marginRight)),
      {
        range() {
          return [marginLeft, width - marginRight];
        },
      }
    );

    let colorBar = svg
      .append("image")
      .attr("x", marginLeft)
      .attr("y", marginTop)
      .attr("width", width - marginLeft - marginRight)
      .attr("height", height - marginTop - marginBottom)
      .attr("preserveAspectRatio", "none")
      .attr("xlink:href", ramp(color.interpolator()).toDataURL());

    if (reverseColor)
      colorBar.attr(
        "transform",
        `translate(${width - marginLeft - marginRight}) scale(-1,1)`
      );

    // scaleSequentialQuantile doesn’t implement ticks or tickFormat.
    if (!x.ticks) {
      if (tickValues === undefined) {
        const n = Math.round(ticks + 1);
        tickValues = d3
          .range(n)
          .map((i) => d3.quantile(color.domain(), i / (n - 1)));
      }
      if (typeof tickFormat !== "function") {
        tickFormat = d3.format(tickFormat === undefined ? ",f" : tickFormat);
      }
    }
  }

  // Threshold
  else if (color.invertExtent) {
    const thresholds = color.thresholds
      ? color.thresholds() // scaleQuantize
      : color.quantiles
      ? color.quantiles() // scaleQuantile
      : color.domain(); // scaleThreshold

    const thresholdFormat =
      tickFormat === undefined
        ? (d) => d
        : typeof tickFormat === "string"
        ? d3.format(tickFormat)
        : tickFormat;

    x = d3
      .scaleLinear()
      .domain([-1, color.range().length - 1])
      .rangeRound([marginLeft, width - marginRight]);

    svg
      .append("g")
      .selectAll("rect")
      .data(color.range())
      .join("rect")
      .call((g) => {
        if (vertical)
          g.attr("x", marginTop)
            .attr("y", (d, i) => x(color.range().length - i - 2))
            .attr("width", height - marginTop - marginBottom)
            .attr("height", (d, i) => x(i) - x(i - 1))
            .attr("fill", (d) => d);
        else
          g.attr("x", (d, i) => x(i - 1))
            .attr("y", marginTop)
            .attr("width", (d, i) => x(i) - x(i - 1))
            .attr("height", height - marginTop - marginBottom)
            .attr("fill", (d) => d);
      });

    // tickValues = tickValues
    //   ? tickValues.map((v) => v / thresholds[0] - 1)
    //   : d3.range(thresholds.length);
    // tickFormat = (i) =>
    //   thresholdFormat(parseFloat(((i + 1) * thresholds[0]).toFixed(1)), i);

    tickValues = d3.range(thresholds.length);
    tickFormat = (i) =>
      thresholdFormat(thresholds[vertical ? thresholds.length - 1 - i : i], i);
  }

  // Ordinal
  else {
    x = d3
      .scaleBand()
      .domain(color.domain())
      .rangeRound([marginLeft, width - marginRight]);

    svg
      .append("g")
      .selectAll("rect")
      .data(color.domain())
      .join("rect")
      .attr("x", x)
      .attr("y", marginTop)
      .attr("width", Math.max(0, x.bandwidth() - 1))
      .attr("height", height - marginTop - marginBottom)
      .attr("fill", color);

    tickAdjust = () => {};
  }
  // console.debug(tickValues);
  svg
    .append("g")
    .attr(
      "transform",
      `translate(${vertical ? [marginTop + 5, 0] : [0, height - marginBottom]})`
    )
    .call(
      d3[vertical ? "axisRight" : "axisBottom"](x)
        .ticks(ticks, typeof tickFormat === "string" ? tickFormat : undefined)
        .tickFormat(typeof tickFormat === "function" ? tickFormat : undefined)
        .tickSize(tickSize)
        .tickValues(tickValues)
    )
    .call(tickAdjust)
    .call((g) => g.select(".domain").remove())
    .call((g) =>
      g
        .append("text")
        .attr("x", vertical ? -marginTop : marginLeft)
        .attr("y", vertical ? -5 : marginTop + marginBottom - height - 6)
        .attr("fill", "currentColor")
        .attr("text-anchor", "start")
        .attr("font-weight", "bold")
        .attr("class", "title")
        .text(title)
    );

  return svg.node();
};

//==減少事件...觸發頻率
export const updateHandler = (
  action,
  updateObj = { updateFlag: true, updateTimeOut: null, updateDelay: 10 },
  mustDone = false
) => {
  // console.debug(parameter)
  // console.debug(chartUpdateObj.updateFlag);

  if (!updateObj.updateFlag) clearTimeout(updateObj.updateTimeOut);

  updateObj.updateTimeOut = setTimeout(() => {
    action.param ? action.fun(...action.param) : action();
    updateObj.updateFlag = true;
  }, updateObj.updateDelay);

  updateObj.updateFlag = mustDone;
};

//==文章排序
export const sortModel = (x, y) => {
  // console.debug(x, y);
  let reg = /\((\d+)([a-b]?)\)/;

  let matchX = reg.exec(x) ?? [0, 0, 0],
    matchY = reg.exec(y) ?? [0, 0, 0];

  let yearX = Number(matchX[1]),
    yearY = Number(matchY[1]);

  let sort = yearY - yearX;
  if (yearY === yearX) sort = matchX[2] < matchY[2] ? 1 : -1;

  return sort;
};

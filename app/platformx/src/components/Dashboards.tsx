import CardFour from './CardFour';
import CardOne from './CardOne';
import CardThree from './CardThree';
import CardTwo from './CardTwo';
import ChartOne from './ChartOne';
import ChartThree from './ChartThree';
import ChartTwo from './ChartTwo';
import ChatCard from './ChatCard';

const ECommerce = () => {
  return (
    <>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 xl:grid-cols-4 2xl:gap-7.5">
        <CardOne />
        <CardTwo />
        <CardThree />
        <CardFour />
      </div>

      <div className="mt-4 grid grid-cols-12 gap-4 md:mt-6 md:gap-6 2xl:mt-7.5 2xl:gap-7.5">
        <ChartOne />
        <ChartTwo />
        <ChartThree />
      </div>
    </>
  );
};

export default ECommerce;

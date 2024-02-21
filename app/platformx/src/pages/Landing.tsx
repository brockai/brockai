import Brockailogo from '../images/logo/brockai.png'

const Landing = () => {

  return (
    <div className="dark:bg-boxdark-2 dark:text-bodydark">
      <div className="flex h-screen overflow-hidden">
        <div className="relative flex flex-1 flex-col overflow-y-auto overflow-x-hidden">
          <img src={Brockailogo} alt="Logo" />
        </div>
      </div>
    </div>
  );
};

export default Landing;

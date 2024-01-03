
import DropdownNotification from './DropdownNotification';
import Logout from './Logout';
import BrockaiLogo from '../images/logo/brockai.png';
import DarkModeSwitcher from '../components/DarkModeSwitcher';

const Header = (props: {
  sidebarOpen: string | boolean | undefined;
  setSidebarOpen: (arg0: boolean) => void;
}) => {
  return (
    <header className="sticky top-0 z-999 flex w-full bg-white drop-shadow-1 dark:bg-boxdark dark:drop-shadow-none">
      <div className="flex flex-grow items-center justify-between py-4 px-4 shadow-2 md:px-6 2xl:px-11">
        <div className="flex items-center gap-3"><img src={BrockaiLogo} style={{ height: '54px' }} alt="brockai" />
          <h1 className="text-title-xl text-logotext">Platform</h1>
        </div>

        <div className="flex items-center 2xsm:gap-7">
          <ul className="flex items-center 2xsm:gap-5">
            <DarkModeSwitcher />
            <DropdownNotification />
            <Logout />
          </ul>
        </div>
      </div>
    </header>
  );
};

export default Header;

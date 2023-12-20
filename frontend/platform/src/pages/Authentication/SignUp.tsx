import OpenSearchSignup from '../../components/OpenSearchSignup'
import SigninSignupIntro from '../../components/SigninSignupIntro'

const SignUp = () => {
  return (
    <>
      <div className="rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
        <div className="flex flex-wrap items-center">
          <div className="hidden w-full xl:block xl:w-1/2">
            <div className="py-17.5 px-26 text-center">
             < SigninSignupIntro />
            </div>
          </div>

          <div className="w-full border-stroke dark:border-strokedark xl:w-1/2 xl:border-l-2">
            <div className="w-full p-4 sm:p-12.5 xl:p-17.5">
              < OpenSearchSignup />
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default SignUp;
